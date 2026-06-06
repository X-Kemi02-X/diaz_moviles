from django.core.exceptions import ValidationError
from django.db import models
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
        self.total = total
        self.save(update_fields=['total'])

    def _ajustar_stock(self, signo):
        for detalle in self.detalles.all():
            Producto.objects.filter(pk=detalle.producto_id).update(
                stock=models.F('stock') + (signo * detalle.cantidad)
            )

    def clean(self):
        if self.estado == 'completada' and self.pk:
            old = Venta.objects.get(pk=self.pk)
            if old.estado != 'completada':
                for detalle in self.detalles.all():
                    if detalle.producto.stock < detalle.cantidad:
                        raise ValidationError(
                            f"Stock insuficiente para {detalle.producto.nombre}: "
                            f"disponible {detalle.producto.stock}, requerido {detalle.cantidad}"
                        )

    def save(self, *args, **kwargs):
        old_estado = None
        if self.pk:
            old_estado = Venta.objects.get(pk=self.pk).estado

        if old_estado != self.estado and self.estado == 'completada':
            for detalle in self.detalles.all():
                if detalle.producto.stock < detalle.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para {detalle.producto.nombre}: "
                        f"disponible {detalle.producto.stock}, requerido {detalle.cantidad}"
                    )

        super().save(*args, **kwargs)

        if old_estado != self.estado:
            if self.estado == 'completada':
                self._ajustar_stock(-1)
            elif old_estado == 'completada' and self.estado in ('cancelada', 'anulada'):
                self._ajustar_stock(+1)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} - ${self.total}"
