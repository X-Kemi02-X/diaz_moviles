import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from tienda.models import Marca, Categoria, Producto, Cliente, Proveedor, Venta, DetalleVenta
from django.contrib.auth.models import User

# Limpiar datos previos
DetalleVenta.objects.all().delete()
Venta.objects.all().delete()
Producto.objects.all().delete()
Categoria.objects.all().delete()
Marca.objects.all().delete()
Cliente.objects.all().delete()
Proveedor.objects.all().delete()

# Crear cliente normal para pruebas
cliente_user, _ = User.objects.get_or_create(username='cliente', defaults={'email': 'cliente@email.com'})
cliente_user.set_password('cliente123')
cliente_user.save()

# 1. Marcas
m1 = Marca.objects.create(nombre='Samsung', pais_origen='Corea del Sur', descripcion='Electrónica coreana')
m2 = Marca.objects.create(nombre='Apple', pais_origen='Estados Unidos', descripcion='Tecnología americana')
m3 = Marca.objects.create(nombre='Xiaomi', pais_origen='China', descripcion='Tecnología china')
m4 = Marca.objects.create(nombre='Motorola', pais_origen='Estados Unidos', descripcion='Teléfonos americanos')
m5 = Marca.objects.create(nombre='Huawei', pais_origen='China', descripcion='Tecnología china')
print(f'Marcas: {Marca.objects.count()}')

# 2. Categorias
c1 = Categoria.objects.create(nombre='Smartphone', descripcion='Teléfonos inteligentes')
c2 = Categoria.objects.create(nombre='Tablet', descripcion='Tabletas electrónicas')
c3 = Categoria.objects.create(nombre='Accesorio', descripcion='Accesorios para móviles')
c4 = Categoria.objects.create(nombre='Smartwatch', descripcion='Relojes inteligentes')
c5 = Categoria.objects.create(nombre='Audífonos', descripcion='Auriculares y headphones')
print(f'Categorías: {Categoria.objects.count()}')

# 3. Productos
Producto.objects.create(nombre='Galaxy S24', marca=m1, categoria=c1, modelo='S24', precio=899.99, stock=15)
Producto.objects.create(nombre='iPhone 15 Pro', marca=m2, categoria=c1, modelo='A3101', precio=1299.99, stock=10)
Producto.objects.create(nombre='Redmi Note 13', marca=m3, categoria=c1, modelo='RN13', precio=299.99, stock=30)
Producto.objects.create(nombre='Moto G84', marca=m4, categoria=c1, modelo='G84', precio=349.99, stock=20)
Producto.objects.create(nombre='Galaxy Tab S9', marca=m1, categoria=c2, modelo='S9', precio=799.99, stock=8)
Producto.objects.create(nombre='iPad Air', marca=m2, categoria=c2, modelo='M2', precio=699.99, stock=12)
Producto.objects.create(nombre='Galaxy Watch 6', marca=m1, categoria=c4, modelo='W6', precio=349.99, stock=25)
Producto.objects.create(nombre='AirPods Pro', marca=m2, categoria=c5, modelo='AP2', precio=249.99, stock=18)
Producto.objects.create(nombre='MatePad 11', marca=m5, categoria=c2, modelo='M11', precio=499.99, stock=5)
Producto.objects.create(nombre='Cargador Rápido', marca=m3, categoria=c3, modelo='CR-01', precio=25.99, stock=50)
Producto.objects.create(nombre='Funda Samsung', marca=m1, categoria=c3, modelo='FS-01', precio=15.99, stock=100)
Producto.objects.create(nombre='Audífonos Xiaomi', marca=m3, categoria=c5, modelo='AX-01', precio=45.99, stock=40)
print(f'Productos: {Producto.objects.count()}')

# 4. Clientes
c = Cliente.objects.create(nombre='Juan', apellido='Pérez', cedula='1234567890', email='juan@email.com', telefono='0991234567')
Cliente.objects.create(nombre='María', apellido='González', cedula='0987654321', email='maria@email.com', telefono='0997654321')
Cliente.objects.create(nombre='Carlos', apellido='López', cedula='1112223330', email='carlos@email.com', telefono='0981112233')
print(f'Clientes: {Cliente.objects.count()}')

# 5. Proveedores
Proveedor.objects.create(nombre='Distribuidora Smart', contacto='Luis Vera', telefono='0999000001', email='luis@dsmart.com')
Proveedor.objects.create(nombre='TecnoImport', contacto='Ana Ruiz', telefono='0999000002', email='ana@tecnoimport.com')
Proveedor.objects.create(nombre='MovilExpress', contacto='Pedro Solís', telefono='0999000003', email='pedro@movilexpress.com')
print(f'Proveedores: {Proveedor.objects.count()}')

# 6. Ventas
admin = User.objects.get(username='admin')
venta = Venta.objects.create(cliente=c, usuario=admin, total=1199.98, estado='completada', metodo_pago='tarjeta')
DetalleVenta.objects.create(venta=venta, producto_id=1, cantidad=1, precio_unitario=899.99, subtotal=899.99)
DetalleVenta.objects.create(venta=venta, producto_id=10, cantidad=2, precio_unitario=25.99, subtotal=51.98)

venta2 = Venta.objects.create(cliente=c, usuario=admin, total=1299.99, estado='pendiente', metodo_pago='efectivo')
DetalleVenta.objects.create(venta=venta2, producto_id=2, cantidad=1, precio_unitario=1299.99, subtotal=1299.99)
print(f'Ventas: {Venta.objects.count()}, Detalles: {DetalleVenta.objects.count()}')
print('\n✅ Datos de prueba listos!')
