from rest_framework import viewsets
from tienda.models.detalle_venta import DetalleVenta
from tienda.serializers.detalle_venta import DetalleVentaSerializer
from tienda.permissions import AdminOrReadOnly


class DetalleVentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleVenta.objects.select_related('producto', 'venta').all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_fields = ['venta', 'producto']
    ordering_fields = ['venta', 'producto', 'cantidad', 'subtotal']
