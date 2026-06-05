from django.db import models
from django.conf import settings
from tienda.models.cliente import Cliente


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

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} - ${self.total}"
