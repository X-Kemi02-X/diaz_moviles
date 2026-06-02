from django.contrib import admin
from tienda.models.marca import Marca
from tienda.models.categoria import Categoria
from tienda.models.producto import Producto
from tienda.models.cliente import Cliente
from tienda.models.proveedor import Proveedor
from tienda.models.venta import Venta
from tienda.models.detalle_venta import DetalleVenta


class ProductoInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais_origen', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'pais_origen']
    list_filter = ['activo']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    search_fields = ['nombre']
    list_filter = ['activo']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'modelo', 'precio', 'stock', 'activo']
    search_fields = ['nombre', 'modelo']
    list_filter = ['activo', 'marca', 'categoria']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'activo']
    search_fields = ['nombre', 'apellido', 'cedula', 'email']
    list_filter = ['activo']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'telefono', 'email', 'activo']
    search_fields = ['nombre', 'contacto']
    list_filter = ['activo']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'total', 'estado', 'metodo_pago']
    list_filter = ['estado', 'metodo_pago']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'cliente__cedula']
    readonly_fields = ['fecha', 'total']
    inlines = [ProductoInline]
