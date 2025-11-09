from django.db import models
from django.contrib.auth.models import User

# Clon seguro de los modelos de ventas/cliente definidos originalmente en `app_shop`.
# Usamos `db_table` apuntando a las tablas existentes y `managed = False` para evitar
# que Django intente crear/alterar las tablas aquí.


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'app_shop_cliente'
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Venta(models.Model):
    # Usamos un related_name distinto para evitar choque con el modelo original en app_shop
    vendedor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ventas_ventas',
        related_query_name='ventas_ventas'
    )
    cliente = models.ForeignKey('ventas.Cliente', on_delete=models.CASCADE, related_name='compras')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.PositiveIntegerField(default=1)
    total_venta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_shop_venta'
        managed = False

    def save(self, *args, **kwargs):
        # Calculamos el total antes de guardar; no vamos a crear tablas nuevas.
        if self.producto and self.producto.precio is not None:
            self.total_venta = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta #{self.pk} - {self.cliente}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey('ventas.Venta', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        db_table = 'app_shop_detalleventa'
        managed = False

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Borrado'}"

    def subtotal(self):
        return self.cantidad * self.precio_unitario
from django.db import models

# Create your models here.
