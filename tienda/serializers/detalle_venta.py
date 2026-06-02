from rest_framework import serializers
from tienda.models.detalle_venta import DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = '__all__'
