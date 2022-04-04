from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

class Supliers(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    address = models.TextField(verbose_name='Адрес')
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Номер телефона необходимо вводить в формате: «+999999999». Допускается до 15 цифр.")
    phone_number = models.CharField(verbose_name='Номер телефона', validators=[phone_regex], max_length=16)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self) -> str:
        return f'{self.name}'

class Details(models.Model):
    name = models.CharField(verbose_name='Название детали', max_length=50)
    vendore_code = models.CharField(verbose_name='Артикул', max_length=50)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self) -> str:
        return f'{self.name} {self.vendore_code}'

class SupplierDetails(models.Model):
    supplier = models.ForeignKey(Supliers, on_delete=models.CASCADE, verbose_name='Поставщик')
    detail = models.ForeignKey(Details, on_delete=models.CASCADE, verbose_name='Деталь')
    cost = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Цена')

    class Meta:
        verbose_name = 'Детали поставщиков'
        verbose_name_plural = 'Детали поставщиков'

    def __str__(self) -> str:
        return f'{self.supplier}, {self.detail}, {self.cost}'

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


class PurchasesSummary(Purchases):

    class Meta:
        proxy = True
        verbose_name = 'Сумма покупок'
        verbose_name_plural = 'Сумма покупок'
