from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from company.models import BranchableModel, BranchManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def _create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(phone=phone, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, BranchableModel, PermissionsMixin):
    class Role(models.TextChoices):
        doctor = 'doctor', 'Доктор',
        registrar = 'registrar', 'Регистратор',
        admin = 'admin', 'Администратор',

    class Status(models.TextChoices):
        active = 'active', 'Активный'
        disabled = 'disabled', 'Не активный'

    fullname = models.CharField(verbose_name='Ф.И.О', max_length=255)
    username = models.CharField(verbose_name='Имя пользователя', max_length=255, unique=True, null=True, blank=True)
    role = models.CharField(verbose_name='Роль', max_length=255, choices=Role.choices)
    phone = models.CharField(verbose_name='Телефон', max_length=20, unique=True)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.active)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    start_time = models.TimeField(verbose_name='Время начала работы', null=True)
    end_time = models.TimeField(verbose_name='Время конца работы', null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )

    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    USERNAME_FIELD = 'phone'
    super_objects = MyUserManager()
    objects = BranchManager()

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
