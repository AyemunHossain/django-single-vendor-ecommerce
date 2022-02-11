# Generated by Django 3.2.8 on 2022-01-13 13:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20220113_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproduct',
            name='active',
        ),
        migrations.RemoveField(
            model_name='product',
            name='active',
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='visibility',
            field=models.IntegerField(choices=[(1, 'Live'), (2, 'Draft')], default=1, verbose_name='Product Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='visibility',
            field=models.IntegerField(choices=[(1, 'Live'), (2, 'Draft')], default=1, verbose_name='Product Status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
