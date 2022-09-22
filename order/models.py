from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        process = 'process', 'В процессе'
        done = 'done', 'Завершённый'
        canceled = 'canceled', 'Отменённый'

    patient = models.ForeignKey('patient.Patient',
                                on_delete=models.PROTECT,
                                verbose_name='Пациент')
    doctor = models.ForeignKey('user.User',
                               on_delete=models.PROTECT,
                               related_name='doctor',
                               verbose_name='Доктор')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.process)
    content = models.TextField(verbose_name='Жалобы', null=True)
    diagnosis = models.TextField(verbose_name='Диагноз', null=True)
    inspection = models.TextField(verbose_name='Осмотр', null=True)
    registrar = models.ForeignKey('user.User',
                                  verbose_name='Регистрировал',
                                  on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.patient} | {self.doctor}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class OrderItem(models.Model):
    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    service = models.ForeignKey('service.Service',
                                on_delete=models.PROTECT,
                                verbose_name='Услуга')
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              verbose_name='Заказ')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    price = models.FloatField(verbose_name='Цена', default=0)
    count = models.IntegerField(verbose_name='Кол-во', default=0)
    amount = models.FloatField(verbose_name='Сумма', default=0)
    tooth = models.IntegerField(verbose_name='Номер зуба', default=0)
    registrar = models.ForeignKey('user.User',
                                  verbose_name='Регистрировал',
                                  on_delete=models.PROTECT)
    content = models.TextField(verbose_name='Контент', null=True)

    def __str__(self):
        return f'{self.service}'

    class Meta:
        verbose_name = 'Элемент заявки'
        verbose_name_plural = 'Элементы заявок'
