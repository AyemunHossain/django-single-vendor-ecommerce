# Generated by Django 3.2.8 on 2022-01-30 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0005_auto_20220130_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
