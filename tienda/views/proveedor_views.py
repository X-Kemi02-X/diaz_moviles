from rest_framework import viewsets
from tienda.models.proveedor import Proveedor
from tienda.serializers.proveedor import ProveedorSerializer
from tienda.permissions import AdminOrReadOnly


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'contacto', 'email', 'telefono']
    ordering_fields = ['nombre', 'fecha_registro']
