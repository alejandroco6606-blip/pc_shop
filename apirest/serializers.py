from rest_framework import serializers
from django.contrib.auth.models import User
from inventario.models import Marca, Proveedor, Categoria, Producto
from ventas.models import Cliente, Venta, DetalleVenta

# ==================== USUARIOS ====================

class UserSerializer(serializers.ModelSerializer):
    """Serializador para información básica de usuarios"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registro de nuevos usuarios"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# ==================== INVENTARIO ====================

class MarcaSerializer(serializers.ModelSerializer):
    """Serializador para marcas"""
    productos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'productos_count']
    
    def get_productos_count(self, obj):
        return obj.productos.count()

class ProveedorSerializer(serializers.ModelSerializer):
    """Serializador para proveedores"""
    productos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'telefono', 'email', 'productos_count']
    
    def get_productos_count(self, obj):
        return obj.productos.count()

class CategoriaSerializer(serializers.ModelSerializer):
    """Serializador para categorías"""
    productos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'productos_count']
    
    def get_productos_count(self, obj):
        return obj.productos.count()

class ProductoSerializer(serializers.ModelSerializer):
    """Serializador para productos con información detallada"""
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'precio', 'descripcion',
            'marca', 'marca_nombre',
            'proveedor', 'proveedor_nombre', 
            'categoria', 'categoria_nombre'
        ]

class ProductoListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listados de productos"""
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'marca_nombre', 'proveedor_nombre', 'categoria_nombre']

# ==================== VENTAS ====================

class ClienteSerializer(serializers.ModelSerializer):
    """Serializador para clientes"""
    compras_count = serializers.SerializerMethodField()
    total_comprado = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'rut', 'nombre', 'apellido', 'email', 
            'telefono', 'direccion', 'compras_count', 'total_comprado'
        ]
    
    def get_compras_count(self, obj):
        return obj.compras.count()
    
    def get_total_comprado(self, obj):
        total = sum(venta.total_venta or 0 for venta in obj.compras.all())
        return total

class DetalleVentaSerializer(serializers.ModelSerializer):
    """Serializador para detalles de venta"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleVenta
        fields = [
            'id', 'producto', 'producto_nombre', 
            'cantidad', 'precio_unitario', 'subtotal'
        ]
    
    def get_subtotal(self, obj):
        return obj.subtotal()

class VentaSerializer(serializers.ModelSerializer):
    """Serializador para ventas con detalles completos"""
    vendedor_nombre = serializers.CharField(source='vendedor.get_full_name', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.__str__', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id', 'vendedor', 'vendedor_nombre',
            'cliente', 'cliente_nombre',
            'producto', 'producto_nombre',
            'cantidad', 'total_venta', 'fecha',
            'detalles'
        ]
        read_only_fields = ['total_venta', 'fecha']

class VentaListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listados de ventas"""
    vendedor_nombre = serializers.CharField(source='vendedor.username', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.__str__', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id', 'vendedor_nombre', 'cliente_nombre', 
            'producto_nombre', 'cantidad', 'total_venta', 'fecha'
        ]

class VentaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear nuevas ventas"""
    class Meta:
        model = Venta
        fields = ['vendedor', 'cliente', 'producto', 'cantidad']
    
    def create(self, validated_data):
        # El método save() del modelo calcula automáticamente el total
        return super().create(validated_data)
