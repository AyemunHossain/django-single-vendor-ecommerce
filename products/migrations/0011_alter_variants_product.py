# Generated by Django 3.2.8 on 2022-01-15 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_images_imagegalary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variants',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', related_query_name='variants', to='products.product'),
        ),
    ]