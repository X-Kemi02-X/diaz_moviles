from rest_framework import viewsets
from tienda.models.venta import Venta
from tienda.serializers.venta import VentaSerializer
from tienda.permissions import AdminOrAuthenticatedWrite


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.select_related('cliente', 'usuario').prefetch_related('detalles__producto').all()
    serializer_class = VentaSerializer
    permission_classes = [AdminOrAuthenticatedWrite]
    filterset_fields = ['estado', 'metodo_pago', 'cliente', 'usuario']
    search_fields = ['observacion']
    ordering_fields = ['fecha', 'total']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
