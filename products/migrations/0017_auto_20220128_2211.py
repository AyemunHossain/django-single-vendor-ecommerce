# Generated by Django 3.2.8 on 2022-01-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20220128_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='is_display',
            field=models.BooleanField(default=False, verbose_name='Is Display'),
        ),
        migrations.AddField(
            model_name='variants',
            name='is_treanding',
            field=models.BooleanField(default=False, verbose_name='Is Display'),
        ),
    ]
