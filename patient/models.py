from django.db import models


class Patient(models.Model):
    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    class DocType(models.TextChoices):
        passport = 'passport', 'Паспорт',
        metrics = 'metrics', 'Метрика'

    class Gender(models.TextChoices):
        male = 'male', 'Мужчина',
        female = 'female', 'Женщина'

    fullname = models.CharField(verbose_name='Ф.И.О', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    image = models.TextField(verbose_name='Фото', blank=True)
    birthday = models.DateField('Дата рождения')
    gender = models.CharField(verbose_name='Пол', choices=Gender.choices, max_length=255)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    last_visit = models.DateTimeField('Дата последнего визита стоматолога', null=True)
    doc_type = models.CharField(verbose_name='Тип документа', max_length=255, choices=DocType.choices)
    doc_series = models.CharField(verbose_name='Серия документа', max_length=255)
    doc_number = models.CharField(verbose_name='Номер документа', max_length=7)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    chat_id = models.BigIntegerField(verbose_name='Телеграм айди', default=0)
    registrar = models.ForeignKey('user.User',
                                  verbose_name='Регистрировал',
                                  on_delete=models.PROTECT)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Record(models.Model):
    patient = models.ForeignKey('Patient',
                                on_delete=models.PROTECT,
                                verbose_name='Пациент')
    doctor = models.ForeignKey('user.User',
                               on_delete=models.PROTECT,
                               verbose_name='Доктор')
    date = models.DateTimeField(verbose_name='Дата записи')
    content = models.TextField(verbose_name='Контент', null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    registrar = models.ForeignKey('user.User',
                                  related_name='registrar',
                                  verbose_name='Регистрировал',
                                  on_delete=models.PROTECT)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient} | {self.doctor} | {self.date}'

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Запись на прием'
