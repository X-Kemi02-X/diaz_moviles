from tienda.views.health import health_check
from tienda.views.marca_views import MarcaViewSet
from tienda.views.categoria_views import CategoriaViewSet
from tienda.views.producto_views import ProductoViewSet
from tienda.views.cliente_views import ClienteViewSet
from tienda.views.proveedor_views import ProveedorViewSet
from tienda.views.venta_views import VentaViewSet
from tienda.views.detalle_venta_views import DetalleVentaViewSet

__all__ = [
    'health_check',
    'MarcaViewSet',
    'CategoriaViewSet',
    'ProductoViewSet',
    'ClienteViewSet',
    'ProveedorViewSet',
    'VentaViewSet',
    'DetalleVentaViewSet',
]
