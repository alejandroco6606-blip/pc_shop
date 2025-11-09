from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('app_shop', '0006_venta_detalleventa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Cliente',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('rut', models.CharField(max_length=12, unique=True)),
                        ('nombre', models.CharField(max_length=100)),
                        ('apellido', models.CharField(max_length=100)),
                        ('email', models.EmailField(blank=True, null=True, max_length=254)),
                        ('telefono', models.CharField(blank=True, null=True, max_length=20)),
                        ('direccion', models.TextField(blank=True, null=True)),
                    ],
                    options={'db_table': 'app_shop_cliente', 'managed': False},
                ),
                migrations.CreateModel(
                    name='Venta',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('cantidad', models.PositiveIntegerField(default=1)),
                        ('total_venta', models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)),
                        ('fecha', models.DateTimeField(auto_now_add=True)),
                        ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='ventas.cliente')),
                        ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='inventario.producto')),
                        ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas_ventas', to=settings.AUTH_USER_MODEL)),
                    ],
                    options={'db_table': 'app_shop_venta', 'managed': False},
                ),
                migrations.CreateModel(
                    name='DetalleVenta',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('cantidad', models.PositiveIntegerField(default=1)),
                        ('precio_unitario', models.DecimalField(max_digits=10, decimal_places=0)),
                        ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta')),
                        ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.producto')),
                    ],
                    options={'db_table': 'app_shop_detalleventa', 'managed': False},
                ),
            ],
        ),
    ]
