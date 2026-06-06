from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets
from tienda.models.cliente import Cliente
from tienda.serializers.cliente import ClienteSerializer
from tienda.permissions import AdminOrReadOnly

User = get_user_model()


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono']
    ordering_fields = ['nombre', 'apellido', 'fecha_registro']

    @transaction.atomic
    def perform_destroy(self, instance):
        if instance.usuario:
            instance.usuario.delete()
        instance.delete()
