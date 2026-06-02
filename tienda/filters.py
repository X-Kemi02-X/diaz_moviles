import django_filters
from tienda.models.producto import Producto


class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')

    class Meta:
        model = Producto
        fields = {
            'marca': ['exact'],
            'categoria': ['exact'],
            'activo': ['exact'],
            'precio': ['exact', 'lt', 'gt'],
            'stock': ['exact', 'lt', 'gt'],
        }
