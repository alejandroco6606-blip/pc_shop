# API REST - PC Shop

Esta documentación describe la API REST del sistema PC Shop, que proporciona acceso programático a todas las funcionalidades del sistema de inventario y ventas.

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para la autenticación. Todos los endpoints (excepto registro y login) requieren autenticación.

### Obtener Token

```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

**Respuesta:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Uso del Token

Incluir en el header de todas las peticiones:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Renovar Token

```bash
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 👤 Registro de Usuarios

### Crear Usuario

```bash
POST /api/auth/register/
Content-Type: application/json

{
    "username": "nuevo_usuario",
    "password": "contraseña123",
    "password_confirm": "contraseña123",
    "email": "usuario@email.com",
    "first_name": "Nombre",
    "last_name": "Apellido"
}
```

## 📦 Inventario

### Marcas

```bash
# Listar marcas
GET /api/marcas/

# Crear marca
POST /api/marcas/
{
    "nombre": "Nueva Marca"
}

# Obtener marca específica
GET /api/marcas/{id}/

# Actualizar marca
PUT /api/marcas/{id}/
{
    "nombre": "Marca Actualizada"
}

# Eliminar marca
DELETE /api/marcas/{id}/

# Productos de una marca
GET /api/marcas/{id}/productos/
```

### Proveedores

```bash
# Listar proveedores (con búsqueda)
GET /api/proveedores/
GET /api/proveedores/?search=nombre_proveedor

# Crear proveedor
POST /api/proveedores/
{
    "nombre": "Nuevo Proveedor",
    "telefono": "+56912345678",
    "email": "proveedor@email.com"
}

# Obtener proveedor específico
GET /api/proveedores/{id}/

# Actualizar proveedor
PUT /api/proveedores/{id}/

# Eliminar proveedor
DELETE /api/proveedores/{id}/

# Productos de un proveedor
GET /api/proveedores/{id}/productos/
```

### Categorías

```bash
# Listar categorías
GET /api/categorias/

# Crear categoría
POST /api/categorias/
{
    "nombre": "Nueva Categoría",
    "descripcion": "Descripción de la categoría"
}

# Productos de una categoría
GET /api/categorias/{id}/productos/
```

### Productos

```bash
# Listar productos (con filtros)
GET /api/productos/
GET /api/productos/?search=nombre_producto
GET /api/productos/?marca=1&proveedor=2
GET /api/productos/?precio_min=100&precio_max=1000
GET /api/productos/?categoria=1

# Crear producto
POST /api/productos/
{
    "nombre": "Nuevo Producto",
    "precio": "299.99",
    "descripcion": "Descripción del producto",
    "marca": 1,
    "proveedor": 2,
    "categoria": 3
}

# Obtener producto específico
GET /api/productos/{id}/

# Actualizar producto
PUT /api/productos/{id}/

# Eliminar producto
DELETE /api/productos/{id}/

# Estadísticas de productos
GET /api/productos/estadisticas/
```

**Respuesta de estadísticas:**
```json
{
    "total_productos": 150,
    "precio_promedio": 299.99,
    "total_marcas": 25,
    "total_proveedores": 15,
    "total_categorias": 8
}
```

## 💰 Ventas

### Clientes

```bash
# Listar clientes (con búsqueda)
GET /api/clientes/
GET /api/clientes/?search=nombre_cliente

# Crear cliente
POST /api/clientes/
{
    "rut": "12345678-9",
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@email.com",
    "telefono": "+56912345678",
    "direccion": "Calle Falsa 123"
}

# Obtener cliente específico
GET /api/clientes/{id}/

# Compras de un cliente
GET /api/clientes/{id}/compras/
```

### Ventas

```bash
# Listar ventas (con filtros)
GET /api/ventas/
GET /api/ventas/?vendedor=1
GET /api/ventas/?cliente=2
GET /api/ventas/?fecha_desde=2024-01-01&fecha_hasta=2024-12-31

# Crear venta
POST /api/ventas/
{
    "cliente": 1,
    "producto": 5,
    "cantidad": 2
}

# Obtener venta específica
GET /api/ventas/{id}/

# Estadísticas de ventas
GET /api/ventas/estadisticas/
```

**Respuesta de estadísticas:**
```json
{
    "total_ventas": 450,
    "total_ingresos": 125000.00,
    "promedio_venta": 277.78,
    "total_clientes": 89
}
```

## 🔍 Búsquedas y Filtros

### Productos
- `?search=texto` - Busca en nombre y descripción
- `?marca=id` - Filtra por marca
- `?proveedor=id` - Filtra por proveedor
- `?categoria=id` - Filtra por categoría
- `?precio_min=valor` - Precio mínimo
- `?precio_max=valor` - Precio máximo

### Proveedores
- `?search=texto` - Busca en nombre y email

### Clientes
- `?search=texto` - Busca en nombre, apellido, RUT y email

### Ventas
- `?vendedor=id` - Filtra por vendedor
- `?cliente=id` - Filtra por cliente
- `?producto=id` - Filtra por producto
- `?fecha_desde=YYYY-MM-DD` - Desde fecha
- `?fecha_hasta=YYYY-MM-DD` - Hasta fecha

## 📊 Paginación

Todas las listas utilizan paginación automática. La respuesta incluye:

```json
{
    "count": 150,
    "next": "http://api.example.com/api/productos/?page=2",
    "previous": null,
    "results": [...]
}
```

## ⚠️ Códigos de Respuesta

- `200` - OK
- `201` - Creado
- `400` - Solicitud incorrecta
- `401` - No autenticado
- `403` - Sin permisos
- `404` - No encontrado
- `500` - Error del servidor

## 🛠️ Ejemplos de Uso

### Ejemplo con cURL

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Usar token para obtener productos
curl -X GET http://localhost:8000/api/productos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# 3. Crear producto
curl -X POST http://localhost:8000/api/productos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Laptop HP",
    "precio":"899.99",
    "descripcion":"Laptop HP Pavilion",
    "marca":1,
    "proveedor":2,
    "categoria":3
  }'
```

### Ejemplo con Python

```python
import requests

# Configuración
BASE_URL = 'http://localhost:8000/api'
credentials = {'username': 'admin', 'password': 'admin123'}

# Obtener token
response = requests.post(f'{BASE_URL}/auth/login/', json=credentials)
token = response.json()['access']

# Headers con autenticación
headers = {'Authorization': f'Bearer {token}'}

# Obtener productos
productos = requests.get(f'{BASE_URL}/productos/', headers=headers)
print(productos.json())

# Crear cliente
nuevo_cliente = {
    'rut': '12345678-9',
    'nombre': 'Juan',
    'apellido': 'Pérez',
    'email': 'juan@email.com'
}
response = requests.post(f'{BASE_URL}/clientes/', json=nuevo_cliente, headers=headers)
print(response.json())
```

### Ejemplo con JavaScript

```javascript
// Configuración
const BASE_URL = 'http://localhost:8000/api';

// Obtener token
async function login(username, password) {
    const response = await fetch(`${BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    localStorage.setItem('token', data.access);
    return data.access;
}

// Función genérica para API
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    const config = {
        method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        config.body = JSON.stringify(data);
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    return await response.json();
}

// Usar la API
async function ejemplo() {
    // Login
    await login('admin', 'admin123');
    
    // Obtener productos
    const productos = await apiCall('/productos/');
    console.log(productos);
    
    // Crear venta
    const nuevaVenta = {
        cliente: 1,
        producto: 5,
        cantidad: 2
    };
    const venta = await apiCall('/ventas/', 'POST', nuevaVenta);
    console.log(venta);
}
```

## 🚀 Instalación y Configuración

### Requisitos
- Django 4.2+
- Django REST Framework 3.14+
- djangorestframework-simplejwt 5.2+

### Configuración en settings.py

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
    'apirest',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### URLs principales

```python
# urls.py
urlpatterns = [
    # ...
    path('api/', include(('apirest.urls', 'apirest'), namespace='api')),
]
```

## 📝 Notas Importantes

1. **Seguridad**: Todos los endpoints requieren autenticación JWT excepto registro y login
2. **CORS**: Configurar apropiadamente para aplicaciones frontend
3. **Throttling**: Considerar implementar limitación de velocidad en producción  
4. **Logs**: La API registra automáticamente todas las operaciones
5. **Testing**: Incluye suite completa de tests unitarios

## 🔧 Troubleshooting

### Error 401 - Unauthorized
- Verificar que el token JWT esté incluido en el header
- Verificar que el token no haya expirado
- Verificar formato: `Authorization: Bearer <token>`

### Error 400 - Bad Request  
- Verificar formato JSON de los datos enviados
- Verificar que todos los campos requeridos estén presentes
- Revisar validaciones específicas del modelo

### Error 404 - Not Found
- Verificar que la URL sea correcta
- Verificar que el recurso exista (ID válido)
- Verificar que el usuario tenga permisos para ver el recurso