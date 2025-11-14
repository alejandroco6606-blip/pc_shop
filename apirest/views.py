from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from inventario.models import Marca, Proveedor, Categoria, Producto
from ventas.models import Cliente, Venta, DetalleVenta
from .serializers import (
    UserSerializer, RegisterSerializer,
    MarcaSerializer, ProveedorSerializer, CategoriaSerializer,
    ProductoSerializer, ProductoListSerializer,
    ClienteSerializer, VentaSerializer, VentaListSerializer, VentaCreateSerializer,
    DetalleVentaSerializer
)

# ==================== AUTENTICACIÓN ====================

class RegisterView(generics.CreateAPIView):
    """Vista para registrar nuevos usuarios"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)

# ==================== USUARIOS ====================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar usuarios (solo lectura)"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# ==================== INVENTARIO ====================

class MarcaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar marcas"""
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener todos los productos de una marca"""
        marca = self.get_object()
        productos = marca.productos.all()
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)

class ProveedorViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar proveedores"""
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Proveedor.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(email__icontains=search)
            )
        return queryset
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener todos los productos de un proveedor"""
        proveedor = self.get_object()
        productos = proveedor.productos.all()
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener todos los productos de una categoría"""
        categoria = self.get_object()
        productos = categoria.productos.all()
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)

class ProductoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar productos"""
    queryset = Producto.objects.select_related('marca', 'proveedor', 'categoria').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        
        # Filtros de búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(descripcion__icontains=search)
            )
        
        # Filtros por relaciones
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(marca_id=marca)
            
        proveedor = self.request.query_params.get('proveedor', None)
        if proveedor:
            queryset = queryset.filter(proveedor_id=proveedor)
            
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        # Filtros de precio
        precio_min = self.request.query_params.get('precio_min', None)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
            
        precio_max = self.request.query_params.get('precio_max', None)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Estadísticas generales de productos"""
        total_productos = self.get_queryset().count()
        precio_promedio = self.get_queryset().aggregate(
            promedio=Sum('precio')
        )['promedio'] or 0
        
        if total_productos > 0:
            precio_promedio = precio_promedio / total_productos
        
        return Response({
            'total_productos': total_productos,
            'precio_promedio': round(precio_promedio, 2),
            'total_marcas': Marca.objects.count(),
            'total_proveedores': Proveedor.objects.count(),
            'total_categorias': Categoria.objects.count(),
        })

# ==================== VENTAS ====================

class ClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(apellido__icontains=search) |
                Q(rut__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset
    
    @action(detail=True, methods=['get'])
    def compras(self, request, pk=None):
        """Obtener todas las compras de un cliente"""
        cliente = self.get_object()
        ventas = cliente.compras.all().order_by('-fecha')
        serializer = VentaListSerializer(ventas, many=True)
        return Response(serializer.data)

class VentaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar ventas"""
    queryset = Venta.objects.select_related('vendedor', 'cliente', 'producto').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VentaCreateSerializer
        elif self.action == 'list':
            return VentaListSerializer
        return VentaSerializer
    
    def get_queryset(self):
        queryset = self.queryset.order_by('-fecha')
        
        # Filtro por vendedor
        vendedor = self.request.query_params.get('vendedor', None)
        if vendedor:
            queryset = queryset.filter(vendedor_id=vendedor)
        
        # Filtro por cliente
        cliente = self.request.query_params.get('cliente', None)
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)
        
        # Filtro por producto
        producto = self.request.query_params.get('producto', None)
        if producto:
            queryset = queryset.filter(producto_id=producto)
        
        # Filtro por fecha
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        if fecha_desde:
            queryset = queryset.filter(fecha__date__gte=fecha_desde)
            
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        if fecha_hasta:
            queryset = queryset.filter(fecha__date__lte=fecha_hasta)
        
        return queryset
    
    def perform_create(self, serializer):
        # Asignar el vendedor actual
        serializer.save(vendedor=self.request.user)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Estadísticas de ventas"""
        queryset = self.get_queryset()
        
        total_ventas = queryset.count()
        total_ingresos = queryset.aggregate(
            total=Sum('total_venta')
        )['total'] or 0
        
        promedio_venta = 0
        if total_ventas > 0:
            promedio_venta = total_ingresos / total_ventas
        
        return Response({
            'total_ventas': total_ventas,
            'total_ingresos': total_ingresos,
            'promedio_venta': round(promedio_venta, 2),
            'total_clientes': Cliente.objects.count(),
        })

class DetalleVentaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar detalles de venta"""
    queryset = DetalleVenta.objects.select_related('venta', 'producto').all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        venta = self.request.query_params.get('venta', None)
        if venta:
            queryset = queryset.filter(venta_id=venta)
        return queryset
