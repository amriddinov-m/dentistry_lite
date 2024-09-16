from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.safestring import mark_safe

from company.choices import CURRENCIES
from company.middleware import get_current_user


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название', unique=True)
    logo = models.ImageField(verbose_name='Лого', upload_to='companies_logo', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="30" height="30" />')
        return 'No logo'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Branch(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, verbose_name='Компания')
    currency = models.CharField(max_length=255, verbose_name='Валюта', choices=CURRENCIES)
    name = models.CharField(max_length=255, verbose_name='Название')
    expiration_date = models.DateField(verbose_name='Дата окончания срока')
    max_count_doctors = models.IntegerField(default=5, verbose_name='Макс. кол-во врачей')
    max_count_administrators = models.IntegerField(default=5, verbose_name='Макс. кол-во администраторов')
    max_count_assistant = models.IntegerField(default=5, verbose_name='Макс. кол-во ассистентов')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class BranchManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        queryset = super().get_queryset()
        if user and user.is_authenticated:
            return queryset.filter(branch=user.branch)
        return queryset.none()


class DefaultManager(models.Manager):
    pass


class BranchableModel(models.Model):
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.branch:
            current_user = get_current_user()
            if current_user and current_user.is_authenticated:
                self.branch = current_user.branch
        super().save(*args, **kwargs)
