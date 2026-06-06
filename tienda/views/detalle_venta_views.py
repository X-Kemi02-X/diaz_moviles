from rest_framework import viewsets
from tienda.models.detalle_venta import DetalleVenta
from tienda.serializers.detalle_venta import DetalleVentaSerializer
from tienda.permissions import AdminOrAuthenticatedWrite


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.select_related('producto', 'venta').all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [AdminOrAuthenticatedWrite]
    filterset_fields = ['venta', 'producto']
    ordering_fields = ['venta', 'producto', 'cantidad', 'subtotal']
