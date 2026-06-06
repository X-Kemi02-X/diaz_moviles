from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from tienda.models.cliente import Cliente

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_staff'] = self.user.is_staff
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    cedula = serializers.CharField()
    telefono = serializers.CharField()
    direccion = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuario ya está registrado")
        return value

    def validate_email(self, value):
        if Cliente.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso")
        return value

    def validate_cedula(self, value):
        if Cliente.objects.filter(cedula=value).exists():
            raise serializers.ValidationError("Esta cédula ya está registrada")
        return value

    @transaction.atomic
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email']
            )
            cliente = Cliente.objects.create(
                usuario=user,
                nombre=validated_data['nombre'],
                apellido=validated_data['apellido'],
                cedula=validated_data['cedula'],
                email=validated_data['email'],
                telefono=validated_data['telefono'],
                direccion=validated_data['direccion']
            )
            return {'user_id': user.id, 'username': user.username, 'email': user.email}
        except IntegrityError:
            raise serializers.ValidationError("Error al crear la cuenta. Intenta de nuevo.")


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({"detail": "Ambos campos son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
    if len(new_password) < 6:
        return Response({"detail": "La contraseña debe tener al menos 6 caracteres"}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(old_password):
        return Response({"detail": "La contraseña actual no es correcta"}, status=status.HTTP_400_BAD_REQUEST)
    if old_password == new_password:
        return Response({"detail": "La nueva contraseña debe ser diferente a la actual"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"detail": "Contraseña actualizada correctamente"})
