from rest_framework import serializers
from tienda.models.venta import Venta
from tienda.models.detalle_venta import DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'
