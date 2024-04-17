# Generated by Django 3.2.3 on 2022-05-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, null=True, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='images/correos')),
            ],
        ),
    ]