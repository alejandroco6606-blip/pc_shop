from django.db import models

# Clon seguro de modelos que existen en `app_shop`.
# Estos modelos usan `db_table` apuntando a las tablas actuales y `managed = False`
# para evitar que Django intente crear o modificar las tablas aquí.


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'app_shop_marca'
        managed = False

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        db_table = 'app_shop_proveedor'
        managed = False

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'app_shop_categoria'
        managed = False

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    marca = models.ForeignKey('inventario.Marca', on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    proveedor = models.ForeignKey('inventario.Proveedor', on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    categoria = models.ForeignKey('inventario.Categoria', on_delete=models.SET_NULL, related_name='productos', null=True, blank=True)

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()

    class Meta:
        db_table = 'app_shop_producto'
        managed = False

    def __str__(self):
        return self.nombre
from django.db import models

# Create your models here.
