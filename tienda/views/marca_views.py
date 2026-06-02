from rest_framework import viewsets
from tienda.models.marca import Marca
from tienda.serializers.marca import MarcaSerializer
from tienda.permissions import AdminOrReadOnly


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['activo', 'pais_origen']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
