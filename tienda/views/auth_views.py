from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from tienda.models.cliente import Cliente


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
    direccion = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuario ya está registrado")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso")
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
            Cliente.objects.create(
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
        try:
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
