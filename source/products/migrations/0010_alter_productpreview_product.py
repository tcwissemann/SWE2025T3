# Generated by Django 4.2.18 on 2025-04-29 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productpreview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productimage'),
        ),
    ]
