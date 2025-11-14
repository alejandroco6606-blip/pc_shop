from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import (
    RegisterView, UserViewSet,
    MarcaViewSet, ProveedorViewSet, CategoriaViewSet, ProductoViewSet,
    ClienteViewSet, VentaViewSet, DetalleVentaViewSet
)

@api_view(['GET'])
def api_home(request):
    """Vista principal de la API"""
    return Response({
        'message': 'API REST de PC Shop',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'login': '/apirest/auth/login/',
                'refresh': '/apirest/auth/refresh/',
                'register': '/apirest/auth/register/',
            },
            'inventario': {
                'productos': '/apirest/productos/',
                'marcas': '/apirest/marcas/',
                'proveedores': '/apirest/proveedores/',
                'categorias': '/apirest/categorias/',
            },
            'ventas': {
                'clientes': '/apirest/clientes/',
                'ventas': '/apirest/ventas/',
                'detalles': '/apirest/detalle-ventas/',
            },
            'usuarios': '/apirest/usuarios/',
        }
    })

# Configuración del router para las API ViewSets
router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'marcas', MarcaViewSet, basename='marcas')
router.register(r'proveedores', ProveedorViewSet, basename='proveedores')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'ventas', VentaViewSet, basename='ventas')
router.register(r'detalle-ventas', DetalleVentaViewSet, basename='detalle-ventas')

app_name = 'apirest'

urlpatterns = [
    # Vista principal
    path('', api_home, name='api_home'),
    
    # Autenticación
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    
    # API endpoints
    path('', include(router.urls)),
]

"""
Estructura de endpoints disponibles:

AUTENTICACIÓN:
- POST /api/auth/login/ - Obtener token JWT
- POST /api/auth/refresh/ - Refrescar token JWT  
- POST /api/auth/register/ - Registrar nuevo usuario

USUARIOS:
- GET /api/usuarios/ - Listar usuarios
- GET /api/usuarios/{id}/ - Detalle de usuario

INVENTARIO:
- GET|POST /api/marcas/ - Listar/crear marcas
- GET|PUT|DELETE /api/marcas/{id}/ - Detalle/editar/eliminar marca
- GET /api/marcas/{id}/productos/ - Productos de una marca

- GET|POST /api/proveedores/ - Listar/crear proveedores  
- GET|PUT|DELETE /api/proveedores/{id}/ - Detalle/editar/eliminar proveedor
- GET /api/proveedores/{id}/productos/ - Productos de un proveedor

- GET|POST /api/categorias/ - Listar/crear categorías
- GET|PUT|DELETE /api/categorias/{id}/ - Detalle/editar/eliminar categoría  
- GET /api/categorias/{id}/productos/ - Productos de una categoría

- GET|POST /api/productos/ - Listar/crear productos
- GET|PUT|DELETE /api/productos/{id}/ - Detalle/editar/eliminar producto
- GET /api/productos/estadisticas/ - Estadísticas de productos

VENTAS:
- GET|POST /api/clientes/ - Listar/crear clientes
- GET|PUT|DELETE /api/clientes/{id}/ - Detalle/editar/eliminar cliente
- GET /api/clientes/{id}/compras/ - Compras de un cliente

- GET|POST /api/ventas/ - Listar/crear ventas
- GET|PUT|DELETE /api/ventas/{id}/ - Detalle/editar/eliminar venta  
- GET /api/ventas/estadisticas/ - Estadísticas de ventas

- GET|POST /api/detalle-ventas/ - Listar/crear detalles de venta
- GET|PUT|DELETE /api/detalle-ventas/{id}/ - Detalle/editar/eliminar detalle

PARÁMETROS DE CONSULTA DISPONIBLES:

Productos:
- ?search=texto - Buscar en nombre y descripción
- ?marca=id - Filtrar por marca
- ?proveedor=id - Filtrar por proveedor  
- ?categoria=id - Filtrar por categoría
- ?precio_min=valor - Precio mínimo
- ?precio_max=valor - Precio máximo

Proveedores:
- ?search=texto - Buscar en nombre y email

Clientes: 
- ?search=texto - Buscar en nombre, apellido, RUT y email

Ventas:
- ?vendedor=id - Filtrar por vendedor
- ?cliente=id - Filtrar por cliente
- ?producto=id - Filtrar por producto
- ?fecha_desde=YYYY-MM-DD - Desde fecha
- ?fecha_hasta=YYYY-MM-DD - Hasta fecha

Detalles de Venta:
- ?venta=id - Filtrar por venta específica
"""
