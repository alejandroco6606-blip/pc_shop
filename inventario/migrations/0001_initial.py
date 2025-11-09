from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('app_shop', '0006_venta_detalleventa'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Marca',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=100, unique=True)),
                    ],
                    options={'db_table': 'app_shop_marca', 'managed': False},
                ),
                migrations.CreateModel(
                    name='Proveedor',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=100, unique=True)),
                        ('telefono', models.CharField(max_length=20, blank=True)),
                        ('email', models.EmailField(blank=True, max_length=254)),
                    ],
                    options={'db_table': 'app_shop_proveedor', 'managed': False},
                ),
                migrations.CreateModel(
                    name='Categoria',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=100, unique=True)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                    ],
                    options={'db_table': 'app_shop_categoria', 'managed': False},
                ),
                migrations.CreateModel(
                    name='Producto',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=100)),
                        ('precio', models.DecimalField(max_digits=10, decimal_places=2)),
                        ('descripcion', models.TextField()),
                        ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='inventario.marca')),
                        ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='inventario.proveedor')),
                        ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='inventario.categoria')),
                    ],
                    options={'db_table': 'app_shop_producto', 'managed': False},
                ),
            ],
        ),
    ]
