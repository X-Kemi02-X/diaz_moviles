from rest_framework import viewsets
from tienda.models.cliente import Cliente
from tienda.serializers.cliente import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_fields = ['activo']
    search_fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono']
    ordering_fields = ['nombre', 'apellido', 'fecha_registro']
