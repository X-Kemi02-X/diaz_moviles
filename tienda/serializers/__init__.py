from tienda.serializers.marca import MarcaSerializer
from tienda.serializers.categoria import CategoriaSerializer
from tienda.serializers.producto import ProductoSerializer
from tienda.serializers.cliente import ClienteSerializer
from tienda.serializers.proveedor import ProveedorSerializer
from tienda.serializers.venta import VentaSerializer, DetalleVentaSerializer

__all__ = [
    'MarcaSerializer',
    'CategoriaSerializer',
    'ProductoSerializer',
    'ClienteSerializer',
    'ProveedorSerializer',
    'VentaSerializer',
    'DetalleVentaSerializer',
]
