from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from inventario.models import Marca, Proveedor, Categoria, Producto
from ventas.models import Cliente

class APIAuthTestCase(APITestCase):
    """Tests para autenticación de la API"""
    
    def setUp(self):
        self.register_url = reverse('api:register')
        self.login_url = reverse('api:token_obtain_pair')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'email': 'test@test.com'
        }
    
    def test_register_user(self):
        """Test de registro de usuario"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_login_user(self):
        """Test de login y obtención de token"""
        # Crear usuario primero
        User.objects.create_user(username='testuser', password='testpass123')
        
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class InventarioAPITestCase(APITestCase):
    """Tests para endpoints de inventario"""
    
    def setUp(self):
        # Crear usuario y autenticarlo
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Crear datos de prueba
        self.marca = Marca.objects.create(nombre='Test Marca')
        self.proveedor = Proveedor.objects.create(nombre='Test Proveedor')
        self.categoria = Categoria.objects.create(nombre='Test Categoria')
    
    def test_list_marcas(self):
        """Test listar marcas"""
        url = reverse('api:marcas-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_producto(self):
        """Test crear producto"""
        url = reverse('api:productos-list')
        data = {
            'nombre': 'Test Producto',
            'precio': '100.00',
            'descripcion': 'Descripción de prueba',
            'marca': self.marca.id,
            'proveedor': self.proveedor.id,
            'categoria': self.categoria.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Producto.objects.filter(nombre='Test Producto').exists())

class VentasAPITestCase(APITestCase):
    """Tests para endpoints de ventas"""
    
    def setUp(self):
        # Crear usuario y autenticarlo
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Crear datos de prueba
        self.cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Test',
            apellido='Cliente'
        )
    
    def test_list_clientes(self):
        """Test listar clientes"""
        url = reverse('api:clientes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_cliente(self):
        """Test crear cliente"""
        url = reverse('api:clientes-list')
        data = {
            'rut': '98765432-1',
            'nombre': 'Nuevo',
            'apellido': 'Cliente',
            'email': 'nuevo@test.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class APIPermissionsTestCase(APITestCase):
    """Tests para permisos de la API"""
    
    def test_unauthenticated_access(self):
        """Test que endpoints requieren autenticación"""
        endpoints = [
            reverse('api:productos-list'),
            reverse('api:marcas-list'),
            reverse('api:clientes-list'),
            reverse('api:ventas-list'),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
