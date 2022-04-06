# Generated by Django 3.2.12 on 2022-04-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detail', '0003_supliers_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supliers',
            name='is_active',
        ),
        migrations.AddField(
            model_name='details',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный товар или нет'),
        ),
    ]
