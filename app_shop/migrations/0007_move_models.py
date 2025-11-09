from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0006_venta_detalleventa'),
        ('inventario', '0001_initial'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        # Remove models from app_shop state only; no DB operations performed here.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name='DetalleVenta'),
                migrations.DeleteModel(name='Venta'),
                migrations.DeleteModel(name='Cliente'),
                migrations.DeleteModel(name='Producto'),
                migrations.DeleteModel(name='Categoria'),
                migrations.DeleteModel(name='Proveedor'),
                migrations.DeleteModel(name='Marca'),
            ],
        ),
    ]
