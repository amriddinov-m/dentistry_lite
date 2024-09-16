from django.db import models


class Cash(models.Model):
    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    class Method(models.TextChoices):
        cash = 'cash', 'Наличные',
        card = 'card', 'Перевод'

    name = models.CharField(verbose_name='Название', max_length=255)
    amount = models.FloatField(verbose_name='Сумма', default=0)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    method = models.CharField(verbose_name='Метод оплаты', max_length=255, choices=Method.choices)
    creator = models.ForeignKey('user.User',
                                verbose_name='Добавил',
                                on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} | Баланс: {self.amount} сум"

    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'


class CashLog(models.Model):
    class Type(models.TextChoices):
        income = 'income', 'Приход'
        outcome = 'outcome', 'Расход'

    class ModelType(models.TextChoices):
        patient = 'patient', 'Пациент'
        service = 'service', 'Услуги'

    class Method(models.TextChoices):
        cash = 'cash', 'Наличные',
        card = 'card', 'Перевод'

    cash_type = models.CharField(verbose_name='Тип оплаты', max_length=255, choices=Type.choices)
    model_type = models.CharField(verbose_name='Категория', max_length=255, choices=ModelType.choices)
    model_id = models.IntegerField(verbose_name='Причина', default=0)
    amount = models.FloatField(verbose_name='Сумма', default=0)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    creator = models.ForeignKey('user.User',
                                verbose_name='Добавил',
                                on_delete=models.PROTECT)
    content = models.TextField(verbose_name='Контент', null=True)
    cash = models.ForeignKey('Cash', verbose_name='Касса', on_delete=models.SET_NULL, null=True)
    method = models.CharField(verbose_name='Метод оплаты', max_length=255, choices=Method.choices,
                              )

    def __str__(self):
        return f"{self.model_type} | Баланс: {self.amount} сум"

    class Meta:
        verbose_name = 'Операция по кассе'
        verbose_name_plural = 'Операции по кассе'
