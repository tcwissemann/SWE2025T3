# Generated by Django 4.2.18 on 2025-05-01 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_productpreview_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='color_mask',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='productimage',
            name='texture_mask',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
