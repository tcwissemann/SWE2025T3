# Generated by Django 4.2.18 on 2025-02-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='printableHeight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='size',
            name='printableWidth',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
