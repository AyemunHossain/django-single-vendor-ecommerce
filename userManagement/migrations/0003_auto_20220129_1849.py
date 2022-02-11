# Generated by Django 3.2.8 on 2022-01-29 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0002_auto_20220129_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('avatar', models.ImageField(blank=True, upload_to='User/%Y/%m/%d/')),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Rather Not Say')], null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('location', models.CharField(blank=True, max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]