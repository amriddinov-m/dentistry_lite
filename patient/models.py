from django.db import models

from company.models import BranchManager, DefaultManager, BranchableModel


class Patient(BranchableModel):
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
    source = models.ForeignKey('patient.PatientSource', on_delete=models.SET_NULL, verbose_name='Источник',
                               null=True)
    registrar = models.ForeignKey('user.User',
                                  verbose_name='Регистрировал',
                                  on_delete=models.PROTECT)

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Appointment(BranchableModel):
    class AppointmentType(models.TextChoices):
        treatment = 'treatment', 'Лечение'
        consultation = 'consultation', 'Консультация'
        diagnostics = 'diagnostics', 'Диагностика'
        inspection = 'inspection', 'Осмотр'
        sanitation = 'sanitation', 'Санация'
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE, verbose_name='Пациент')
    appointment_type = models.CharField(max_length=255, verbose_name='Тип записи',
                                        choices=AppointmentType.choices,
                                        default=AppointmentType.treatment)
    doctor = models.ForeignKey('user.User', related_name='appointments', on_delete=models.PROTECT, verbose_name='Доктор')
    appointment_date = models.DateTimeField(verbose_name='Назначенная дата')
    duration = models.IntegerField(default=30, verbose_name='Длительность')
    description = models.TextField(verbose_name='Описание', null=True)
    creator = models.ForeignKey('user.User',
                                verbose_name='Добавил', null=True,
                                on_delete=models.PROTECT)

    sent = models.BooleanField(default=False)

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return f'Запись для {self.patient} к {self.doctor} на {self.appointment_date}'

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Запись на прием'


class PatientSource(BranchableModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    objects = BranchManager()
    all_objects = DefaultManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник пациентов'
        verbose_name_plural = 'Источник пациентов'
