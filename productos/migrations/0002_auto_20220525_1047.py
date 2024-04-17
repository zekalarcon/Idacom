# Generated by Django 3.2.3 on 2022-05-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='especial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_tachado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]
