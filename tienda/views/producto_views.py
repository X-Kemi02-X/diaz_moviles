from rest_framework import viewsets
from tienda.models.producto import Producto
from tienda.serializers.producto import ProductoSerializer
from tienda.permissions import AdminOrReadOnly


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('marca', 'categoria').all()
    serializer_class = ProductoSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['activo', 'marca', 'categoria']
    search_fields = ['nombre', 'modelo', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'stock', 'fecha_creacion']
