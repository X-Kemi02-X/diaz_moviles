from rest_framework import viewsets
from tienda.models.categoria import Categoria
from tienda.serializers.categoria import CategoriaSerializer
from tienda.permissions import AdminOrReadOnly


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
