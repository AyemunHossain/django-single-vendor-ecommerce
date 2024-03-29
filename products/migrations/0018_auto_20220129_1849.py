# Generated by Django 3.2.8 on 2022-01-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20220128_2211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalproduct',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical product', 'verbose_name_plural': 'historical Product'},
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
