import datetime

import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView, CreateView

from order.models import Order
from patient.logic import get_appointments
from patient.models import Appointment, Patient
from user.forms import LoginForm, UserForm
from user.logic import delete_doctor, update_status_doctor
from user.models import User

BOT_TOKEN = '5572492160:AAEL_pd6CsZ5ZSo2rAUkOWX9H-iTo8wamV4'


class DoctorActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DoctorActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST

        user = self.request.user
        action = self.request.POST.get('action', None)

        actions = {
            'update_status_doctor': update_status_doctor,
            'delete_doctor': delete_doctor,
            'get_appointments': get_appointments,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        if action == 'get_appointments':
            return JsonResponse(response, safe=True)
        return redirect(back_url)


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        filter_dict = {'doctor': self.request.user.id}
        context['appointments'] = Appointment.objects.filter(**filter_dict)
        context['doctors'] = User.objects.filter(role__in=['doctor', 'admin'])
        context['orders'] = Order.objects.all()

        return context


def send_sms(request):
    datetime_now = datetime.datetime.now()
    appointments = Appointment.objects.filter(date__year=datetime_now.year,
                                              date__month=datetime_now.month,
                                              date__day=datetime_now.day,
                                              sent=False,
                                              patient__chat_id__isnull=False)
    for appointment in appointments:
        if appointment.patient.gender == 'male':
            gender_text = 'Уважаемый'
        else:
            gender_text = 'Уважаемая'
        text = f'{gender_text}, {appointment.patient.fullname}\n\n' \
               f'🕘 Напоминаем вам, что вы записаны сегодня в {appointment.date.strftime("%Y-%m-%d %H:%M")}\n' \
               f'🦷 На прием к стоматологу {appointment.doctor.fullname} \n\n' \
               f'👨🏻‍⚕ Администратор клиники "Центр ортодонтии"\n\n' \
               f'📞 +998(98) 273-52-00\n'
        data = {
            'chat_id': appointment.patient.chat_id,
            'text': text
        }
        location_data = {
            'chat_id': appointment.patient.chat_id,
            'latitude': '39.662252',
            'longitude': '66.941450',
        }
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        location_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendLocation'

        response = requests.post(url, data)
        requests.post(location_url, location_data)
        appointment.sent = True
        appointment.save()
    return render(request, 'bot/list.html', {'appointments': appointments})


def send_notification(request, pk):
    appointment = Appointment.objects.get(pk=pk)

    if appointment.patient.gender == 'male':
        gender_text = 'Уважаемый'
    else:
        gender_text = 'Уважаемая'
    text = f'{gender_text}, {appointment.patient.fullname}\n\n' \
           f'🕘 Напоминаем вам, что вы записаны сегодня в {appointment.date.strftime("%Y-%m-%d %H:%M")}\n' \
           f'🦷 На прием к стоматологу {appointment.doctor.fullname} \n\n' \
           f'👨🏻‍⚕ Администратор клиники "Центр ортодонтии"\n\n' \
           f'📞 +998(98) 273-52-00\n'
    data = {
        'chat_id': appointment.patient.chat_id,
        'text': text
    }
    location_data = {
        'chat_id': appointment.patient.chat_id,
        'latitude': '39.662252',
        'longitude': '66.941450',
    }
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    location_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendLocation'

    response = requests.post(url, data)
    requests.post(location_url, location_data)
    appointment.sent = True
    appointment.save()
    return redirect(reverse('appointment_list'))


class DoctorListView(TemplateView):
    template_name = 'doctor/list.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        context['doctors'] = User.objects.exclude(is_superuser=True)
        return context


class DoctorCreateView(CreateView):
    template_name = 'doctor/create.html'
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('doctor_list')


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone=cd['phone'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home-view'))
                else:
                    context['error'] = 'Disabled account'
            else:
                context['error'] = 'Invalid phone number or password'
        return self.render_to_response(context)


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


class DoctorUpdateView(UpdateView):
    template_name = 'doctor/update.html'
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('doctor_list')


class SslFiles(TemplateView):
    template_name = 'ssl_files.html'
    content_type = 'text/plain'


class WebAppView(TemplateView):
    template_name = 'webapp/old.html'


range_list = range(1, 1000)
