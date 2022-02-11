# Generated by Django 3.2.8 on 2022-01-30 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userManagement.validators


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0004_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True, validators=[userManagement.validators.validate_birthday]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]