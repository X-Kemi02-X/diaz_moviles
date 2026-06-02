from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre
