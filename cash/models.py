from django.db import models

from company.models import BranchManager, DefaultManager, BranchableModel


class Cash(BranchableModel):
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

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return f"{self.name} | Баланс: {self.amount} сум"

    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'


class CashLog(BranchableModel):
    class Type(models.TextChoices):
        income = 'income', 'Приход'
        outcome = 'outcome', 'Расход'

    class ModelType(models.TextChoices):
        patient = 'patient', 'Пациент'
        service = 'service', 'Услуги'
        user = 'user', 'Сотрудник'
        order = 'order', 'Санация'

    class Method(models.TextChoices):
        cash = 'cash', 'Наличные'
        card = 'card', 'Перевод'

    class Category(models.TextChoices):
        order_payment = 'service_payment', 'Оплата за санацию (услугу)'
        staff_salary = 'staff_salary', 'Зарплата персонала'
        service_expense = 'service_expense', 'Расход на услугу'
        rent_and_utility_bills = 'rent_and_utility_bills', 'Аренда и коммунальные платежи'
        purchase_medical_materials = 'purchase_medical_materials', 'Закупка медицинских материалов'

    cash_type = models.CharField(verbose_name='Тип оплаты', max_length=255, choices=Type.choices)
    category = models.CharField(max_length=255, verbose_name='Категория', choices=Category.choices,
                                default=Category.order_payment)
    model_type = models.CharField(verbose_name='Категория', max_length=255, choices=ModelType.choices)
    model_id = models.IntegerField(verbose_name='Причина', default=0)
    amount = models.FloatField(verbose_name='Сумма', default=0)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    creator = models.ForeignKey('user.User',
                                verbose_name='Добавил',
                                on_delete=models.PROTECT)
    content = models.TextField(verbose_name='Контент', null=True)
    cash = models.ForeignKey('Cash', verbose_name='Касса', on_delete=models.SET_NULL, null=True)
    method = models.CharField(verbose_name='Метод оплаты', max_length=255, choices=Method.choices)

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return f"{self.model_type} | Баланс: {self.amount} сум"

    class Meta:
        verbose_name = 'Операция по кассе'
        verbose_name_plural = 'Операции по кассе'
