from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from tienda.views.health import health_check
from tienda.views.marca_views import MarcaViewSet
from tienda.views.categoria_views import CategoriaViewSet
from tienda.views.producto_views import ProductoViewSet
from tienda.views.cliente_views import ClienteViewSet
from tienda.views.proveedor_views import ProveedorViewSet
from tienda.views.venta_views import VentaViewSet
from tienda.views.detalle_venta_views import DetalleVentaViewSet

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)

urlpatterns = [
    path('health/', health_check),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
