"""Script para crear y eliminar datos de prueba en la BD del proyecto.
Uso:
  python scripts/create_test_data.py        # crea los datos de prueba (si no existen)
  python scripts/create_test_data.py --cleanup  # elimina los datos creados (busca prefijos ZZ_TEST_)

Este script añade el directorio raíz al sys.path y configura Django antes de usar el ORM.
Los registros creados usan prefijos "ZZ_TEST_" en nombre/rut para poder identificarlos.
"""
import os
import sys
import django
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_shop.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Categoria, Producto, Marca, Proveedor
from ventas.models import Cliente, Venta
from django.db import transaction

PREFIX = 'ZZ_TEST_'
RUT_PREFIX = 'ZT'


def create_test_user():
    username = PREFIX + 'USER'
    user, created = User.objects.get_or_create(username=username, defaults={'is_active': True})
    if created:
        user.set_password('testpass')
        user.save()
    return user


def create_categories(n=6):
    created = []
    for i in range(1, n+1):
        name = f"{PREFIX}CAT_{i}"
        obj, exists = Categoria.objects.get_or_create(nombre=name, defaults={'descripcion': 'Categoría de prueba'})
        created.append(obj)
    return created


def create_clients(n=6):
    created = []
    for i in range(1, n+1):
        # rut must fit the column (max_length=12 in the original model)
        rut = f"{RUT_PREFIX}{i:03d}"
        nombre = f"{PREFIX}CLIENT_{i}"
        obj, exists = Cliente.objects.get_or_create(rut=rut, defaults={'nombre': nombre, 'apellido': 'Test', 'email': f'test{i}@example.com'})
        created.append(obj)
    return created


def create_products(categories, n=6):
    created = []
    for i in range(1, n+1):
        name = f"{PREFIX}PROD_{i}"
        precio = 1000 * i
        categoria = categories[(i-1) % len(categories)] if categories else None
        obj, exists = Producto.objects.get_or_create(nombre=name, defaults={'precio': precio, 'descripcion': 'Producto de prueba', 'categoria': categoria})
        # Si existe y no tiene precio, intentar actualizar
        if not exists and (obj.precio is None or obj.precio == 0):
            obj.precio = precio
            obj.save()
        created.append(obj)
    return created


def create_sales(user, clients, products, n=6):
    created = []
    for i in range(1, n+1):
        cliente = clients[(i-1) % len(clients)]
        producto = products[(i-1) % len(products)]
        cantidad = (i % 3) + 1
        with transaction.atomic():
            venta = Venta(vendedor=user, cliente=cliente, producto=producto, cantidad=cantidad)
            venta.save()
            created.append(venta)
    return created


def cleanup_test_data():
    # Eliminar ventas creadas
    ventas = Venta.objects.filter(cliente__nombre__startswith(PREFIX)) | Venta.objects.filter(producto__nombre__startswith(PREFIX))
    ventas_count = ventas.count()
    ventas.delete()
    # Eliminar productos
    prod_count = Producto.objects.filter(nombre__startswith(PREFIX)).count()
    Producto.objects.filter(nombre__startswith(PREFIX)).delete()
    # Eliminar clientes
    client_count = Cliente.objects.filter(nombre__startswith(PREFIX)).count()
    Cliente.objects.filter(nombre__startswith(PREFIX)).delete()
    # Eliminar categorias
    cat_count = Categoria.objects.filter(nombre__startswith(PREFIX)).count()
    Categoria.objects.filter(nombre__startswith(PREFIX)).delete()
    # Nota: no eliminamos usuario automáticamente por seguridad
    return {'ventas_deleted': ventas_count, 'productos_deleted': prod_count, 'clientes_deleted': client_count, 'categorias_deleted': cat_count}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cleanup', action='store_true', help='Eliminar los datos de prueba creados anteriormente')
    args = parser.parse_args()

    if args.cleanup:
        res = cleanup_test_data()
        print('Cleanup complete:', res)
        sys.exit(0)

    user = create_test_user()
    cats = create_categories()
    clients = create_clients()
    products = create_products(cats)
    sales = create_sales(user, clients, products)

    print('Creación completada:')
    print('Usuario:', user.username)
    print('Categorias creadas:', len(cats))
    print('Clientes creados:', len(clients))
    print('Productos creados:', len(products))
    print('Ventas creadas:', len(sales))
    print('\nSi quieres limpiar estos datos, ejecuta:\n  python scripts/create_test_data.py --cleanup')
