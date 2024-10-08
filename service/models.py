from django.db import models

from company.models import BranchManager, DefaultManager, BranchableModel


class ServiceCategory(BranchableModel):
    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    name = models.CharField(verbose_name='Название', max_length=255)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'


class Service(models.Model):
    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Цена')
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    category = models.ForeignKey('ServiceCategory',
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
