from django.db.models.signals import pre_save
from django.dispatch import receiver

from company.middleware import get_current_user
from company.models import BranchableModel
from service.models import ServiceCategory


# @receiver(pre_save)
# def assign_branch(sender, instance, **kwargs):
#     # Проверяем, является ли модель наследником BranchableModel
#     if issubclass(sender, BranchableModel):
#         current_user = get_current_user()
#         if current_user and current_user.is_authenticated and not instance.branch:
#             # Присваиваем филиал текущего пользователя, если его нет
#             instance.branch = current_user.branch
#             # instance.save()
