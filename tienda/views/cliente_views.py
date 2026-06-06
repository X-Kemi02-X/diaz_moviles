from django.contrib.auth import get_user_model
from rest_framework import viewsets
from tienda.models.cliente import Cliente
from tienda.serializers.cliente import ClienteSerializer

User = get_user_model()


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_fields = ['activo']
    search_fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono']
    ordering_fields = ['nombre', 'apellido', 'fecha_registro']

    def perform_destroy(self, instance):
        if instance.usuario:
            instance.usuario.delete()
        instance.delete()
