# Generated by Django 4.0.3 on 2024-09-23 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='companies_logo', verbose_name='Лого')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', '$'), ('UZS', 'сўм'), ('RUB', '₽'), ('KZT', '₸'), ('EUR', '€'), ('UAH', '₴')], max_length=255, verbose_name='Валюта')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('expiration_date', models.DateField(verbose_name='Дата окончания срока')),
                ('max_count_doctors', models.IntegerField(default=5, verbose_name='Макс. кол-во врачей')),
                ('max_count_administrators', models.IntegerField(default=5, verbose_name='Макс. кол-во администраторов')),
                ('max_count_assistant', models.IntegerField(default=5, verbose_name='Макс. кол-во ассистентов')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
    ]
