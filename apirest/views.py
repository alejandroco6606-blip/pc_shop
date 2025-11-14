from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Producto, Proveedor
from .serializers import ProductoSerializer, ProveedorSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Vista para registrar usuarios
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Vista para Proveedores
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

# Vista para Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Lógica adicional si es necesario
        serializer.save()
