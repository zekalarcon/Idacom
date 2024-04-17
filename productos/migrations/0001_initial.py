# Generated by Django 3.2.3 on 2022-05-16 21:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('nombre_abreviado', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(blank=True, default='', max_length=200, null=True)),
                ('calificacion', models.DecimalField(decimal_places=1, default=4.1, max_digits=10)),
                ('disponible', models.BooleanField(default=None)),
                ('combo', models.BooleanField(default=None)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=100)),
                ('precio_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                ('sku', models.CharField(default='', max_length=5, unique=True)),
                ('e_a_n', models.CharField(default='', max_length=20)),
                ('bar_code', models.ImageField(blank=True, null=True, upload_to='images/barcode')),
                ('imagen_portada', models.ImageField(blank=True, null=True, upload_to='images/portada')),
                ('descripcion', models.TextField(default='Descripcion', max_length=400, null=True)),
                ('caracteristicas', models.TextField(default='Caracteristicas', max_length=400, null=True)),
                ('fecha_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('categoria', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='ProductosCalificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compra_id', models.IntegerField(blank=True, null=True)),
                ('calificacion', models.DecimalField(decimal_places=1, default=0, max_digits=10)),
                ('comentario', models.TextField(blank=True, default='', max_length=400, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsCombo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='productos.producto')),
                ('productos', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='productoss', to='productos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenesProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagenes', models.FileField(upload_to='images/details')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
    ]