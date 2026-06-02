from django.db import models
from tienda.models.marca import Marca
from tienda.models.categoria import Categoria


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    modelo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True)
    especificaciones = models.JSONField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, max_length=500)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.marca} {self.nombre} ({self.modelo})"
