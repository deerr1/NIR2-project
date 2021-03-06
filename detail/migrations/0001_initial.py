# Generated by Django 3.2.12 on 2022-04-03 19:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название детали')),
                ('vendore_code', models.CharField(max_length=50, verbose_name='Артикул')),
            ],
            options={
                'verbose_name': 'Деталь',
                'verbose_name_plural': 'Детали',
            },
        ),
        migrations.CreateModel(
            name='Supliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Номер телефона необходимо вводить в формате: «+999999999». Допускается до 15 цифр.', regex='^\\+\\d{8,15}$')], verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='SupplierDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detail.details', verbose_name='Деталь')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detail.supliers', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Детали поставщиков',
                'verbose_name_plural': 'Детали поставщиков',
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('date', models.DateField(verbose_name='Дата покупки')),
                ('suplier_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detail.supplierdetails', verbose_name='Деталь')),
            ],
            options={
                'verbose_name': 'Покупки',
                'verbose_name_plural': 'Покупки',
                'ordering': ['-date'],
            },
        ),
    ]
