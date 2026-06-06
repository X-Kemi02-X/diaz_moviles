from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.conf import settings
from tienda.models.cliente import Cliente
from tienda.models.producto import Producto


class Venta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('anulada', 'Anulada'),
    ]
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('otros', 'Otros'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    observacion = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']

    def recalcular_total(self):
        total = self.detalles.aggregate(total=models.Sum('subtotal'))['total'] or 0
        Venta.objects.filter(pk=self.pk).update(total=total)

    def _ajustar_stock(self, signo):
        detalles = self.detalles.select_related('producto').all()
        for detalle in detalles:
            qty = detalle.cantidad
            if signo == -1:
                updated = Producto.objects.filter(
                    pk=detalle.producto_id, stock__gte=qty
                ).update(stock=models.F('stock') - qty)
                if updated == 0:
                    raise ValidationError(
                        f"Stock insuficiente para {detalle.producto.nombre}"
                    )
            else:
                Producto.objects.filter(pk=detalle.producto_id).update(
                    stock=models.F('stock') + qty
                )

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_estado = None
        if not is_new:
            old_estado = Venta.objects.filter(pk=self.pk).values_list('estado', flat=True).first()

        estado_cambio = old_estado is not None and old_estado != self.estado

        if estado_cambio and self.estado == 'completada':
            detalles = self.detalles.select_related('producto').select_for_update(
                of=('producto',)
            ).all()
            for detalle in detalles:
                if detalle.producto.stock < detalle.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para {detalle.producto.nombre}: "
                        f"disponible {detalle.producto.stock}, requerido {detalle.cantidad}"
                    )

        super().save(*args, **kwargs)

        if estado_cambio:
            if self.estado == 'completada':
                self._ajustar_stock(-1)
            elif old_estado == 'completada' and self.estado in ('cancelada', 'anulada'):
                self._ajustar_stock(+1)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} - ${self.total}"
