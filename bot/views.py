from django.shortcuts import render
from django.views.generic import TemplateView

from user.models import User


class HomePageView(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateAppointmentView(TemplateView):
    template_name = 'webapp/create_appointment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = User.super_objects.all()
        return context


class UserProfileView(TemplateView):
    template_name = 'webapp/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserUpdateView(TemplateView):
    template_name = 'webapp/user_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(pk)
        # context['user'] = User.objects.get(id=pk)
        return context
