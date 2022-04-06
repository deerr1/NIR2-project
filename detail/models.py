from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime


class Supliers(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    address = models.TextField(verbose_name='Адрес')
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Номер телефона необходимо вводить в формате: «+999999999». Допускается до 15 цифр.")
    phone_number = models.CharField(verbose_name='Номер телефона', validators=[phone_regex], max_length=16, help_text='Например +795271941111')
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self) -> str:
        return f'{self.name}'

class Details(models.Model):
    name = models.CharField(verbose_name='Название детали', max_length=50)
    vendore_code = models.CharField(verbose_name='Артикул', max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name='Активный товар или нет', default=True)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self) -> str:
        return f'{self.name} {self.vendore_code}'

    def delete(self, instanse, *args, **kwargs):
        self.is_active = False
        super(Details, self).save(*args, **kwargs)

class DeletedDetails(Details):

    class Meta:
        proxy = True
        verbose_name = 'Удаленная деталь'
        verbose_name_plural = 'Удаленные детали'

class SupplierDetails(models.Model):
    supplier = models.ForeignKey(Supliers, on_delete=models.CASCADE, verbose_name='Поставщик')
    detail = models.ForeignKey(Details, on_delete=models.CASCADE, verbose_name='Деталь')
    cost = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Цена')
    is_active = models.BooleanField(verbose_name='Активный товар или нет', default=True)
    deleted_datetime = models.DateTimeField(verbose_name='Дата и время удаления', blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Детали поставщиков'
        verbose_name_plural = 'Детали поставщиков'

    def __str__(self) -> str:
        return f'{self.supplier}, Деталь: {self.detail}, Цена: {self.cost}'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_datetime = datetime.utcnow()
        super(SupplierDetails, self).save(*args, **kwargs)

    @receiver(post_delete, sender=Details)
    def deleted_detail(self, *args, **kwargs):
        self.is_active = False
        self.deleted_datetime = datetime.now()
        super(SupplierDetails, self).save(*args, **kwargs)

class DeletedSupplierDetails(SupplierDetails):

    class Meta:
        proxy = True
        verbose_name = 'Удаленные детали поставщиков'
        verbose_name_plural = 'Удаленные детали поставщиков'

class Purchases(models.Model):
    suplier_detail = models.ForeignKey(SupplierDetails, on_delete=models.CASCADE, verbose_name='Деталь')
    quantity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Количество')
    date = models.DateField(verbose_name='Дата покупки')
    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'
        ordering = ['-date']

    def __str__(self) -> str:
        return f'{self.suplier_detail}, кол-во: {self.quantity}, дата: {self.date}'

    def calculate_sum(self):
        return self.suplier_detail.cost * self.quantity
    sum = property(calculate_sum)

class PurchasesSummary(Purchases):

    class Meta:
        proxy = True
        verbose_name = 'Сумма покупок'
        verbose_name_plural = 'Сумма покупок'
