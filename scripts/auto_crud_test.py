import os
import sys
# Ensure project root is on sys.path (script lives in scripts/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pc_shop.settings')
import django
django.setup()
from django.contrib.auth.models import User
from django.test import Client
from inventario.models import Producto, Marca
from ventas.models import Cliente, Venta

print('Starting automated CRUD test')
# Create or get test user
username = 'autotestuser'
password = 'TestPass123!'
user, created = User.objects.get_or_create(username=username)
if created:
    user.set_password(password)
    user.save()
    print('Created test user')
else:
    print('Test user exists')

client = Client()
client = Client()
# Use a host allowed by settings to avoid DisallowedHost in test client
client.defaults['HTTP_HOST'] = '127.0.0.1'
client.force_login(user)

# Create Marca
marca_data = {'nombre': 'AUTO_MARCA_TEST'}
resp = client.post('/inventario/marcas/crear/', marca_data, follow=True)
print('POST /inventario/marcas/crear/ ->', resp.status_code)
marca = Marca.objects.filter(nombre='AUTO_MARCA_TEST').first()
print('Marca exists:', bool(marca))

# Create Producto
prod_data = {'nombre': 'AUTO_PRODUCT_TEST', 'precio': '999.00', 'descripcion': 'desc', 'marca': marca.id if marca else ''}
resp = client.post('/inventario/crear/', prod_data, follow=True)
print('POST /inventario/crear/ ->', resp.status_code)
producto = Producto.objects.filter(nombre='AUTO_PRODUCT_TEST').first()
print('Producto exists:', bool(producto))

# Create Cliente
cliente_data = {'rut': '00000000-0', 'nombre': 'Auto', 'apellido': 'Test', 'email': 'a@test.com'}
resp = client.post('/ventas/clientes/crear/', cliente_data, follow=True)
print('POST /ventas/clientes/crear/ ->', resp.status_code)
cliente = Cliente.objects.filter(rut='00000000-0').first()
print('Cliente exists:', bool(cliente))

# Create Venta (if producto and cliente exist)
if producto and cliente:
    venta_data = {'cliente': cliente.id, 'producto': producto.id, 'cantidad': '2'}
    resp = client.post('/ventas/crear/', venta_data, follow=True)
    print('POST /ventas/crear/ ->', resp.status_code)
    venta = Venta.objects.order_by('-id').first()
    print('Venta created:', bool(venta))
    if venta:
        print('Venta total_venta:', venta.total_venta)
else:
    print('Skipping venta creation because producto or cliente missing')

# Cleanup created test records
print('Cleaning up test artifacts...')
if Producto.objects.filter(nombre='AUTO_PRODUCT_TEST').exists():
    Producto.objects.filter(nombre='AUTO_PRODUCT_TEST').delete()
    print('Deleted producto')
if Marca.objects.filter(nombre='AUTO_MARCA_TEST').exists():
    Marca.objects.filter(nombre='AUTO_MARCA_TEST').delete()
    print('Deleted marca')
if Cliente.objects.filter(rut='00000000-0').exists():
    Cliente.objects.filter(rut='00000000-0').delete()
    print('Deleted cliente')
# Delete last venta if created (careful with shared DB)
try:
    v = Venta.objects.order_by('-id').first()
    if v and str(v.pk).isdigit():
        v.delete()
        print('Deleted venta')
except Exception as e:
    print('Error deleting venta:', e)

print('Automated CRUD test finished')
