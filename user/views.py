from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView, CreateView

from order.models import Order
from patient.models import Record, Patient
from user.forms import LoginForm
from user.logic import delete_doctor, update_status_doctor
from user.models import User


class DoctorActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DoctorActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        print(post_request)
        user = self.request.user
        action = self.request.POST.get('action', None)
        print(action)
        actions = {
            'update_status_doctor': update_status_doctor,
            'delete_doctor': delete_doctor,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        return redirect(back_url)


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['records'] = Record.objects.all()
        context['patients'] = Patient.objects.all()
        context['doctors'] = User.objects.filter(role='doctor')
        context['orders'] = Order.objects.all()

        return context


class DoctorListView(TemplateView):
    template_name = 'doctor/list.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        context['doctors'] = User.objects.exclude(is_superuser=True)
        return context


class DoctorCreateView(CreateView):
    template_name = 'doctor/create.html'
    model = User
    fields = ['fullname', 'address', 'phone', 'birthday', 'start_time', 'end_time', 'username', 'password', 'role']

    def get_success_url(self):
        return reverse('doctor_list')


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'back_url' in request.POST:
                        return redirect(request.POST['back_url'])
                    return redirect(reverse('home-view'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class DoctorUpdateView(UpdateView):
    template_name = 'doctor/update.html'
    model = User
    fields = ['fullname', 'phone', 'address', 'birthday', 'start_time', 'end_time', 'role', 'username']

    def get_success_url(self):
        return reverse('doctor_list')


class SslFiles(TemplateView):
    template_name = 'ssl_files.html'
