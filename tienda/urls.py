from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tienda.views.health import health_check

router = DefaultRouter()

urlpatterns = [
    # Tu ruta personalizada para verificar que la tienda está online
    path('health/', health_check),
    path('', include(router.urls)),
]