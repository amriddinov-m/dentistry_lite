from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView

from order.models import Order
from patient.logic import create_patient, delete_patient, create_appointment, delete_appointment, \
    send_sms_today_patients, update_appointment_date
from patient.models import Patient, Appointment
from user.models import User


class PatientActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST

        user = self.request.user
        action = self.request.POST.get('action', None)

        actions = {
            'create_patient': create_patient,
            'delete_patient': delete_patient,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        return redirect(back_url)


class AppointmentActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user = self.request.user
        action = self.request.POST.get('action', None)
        actions = {
            'create_appointment': create_appointment,
            'delete_appointment': delete_appointment,
            'send_sms_today_patients': send_sms_today_patients,
            'update_appointment_date': update_appointment_date,

        }
        response = actions[action](post_request, user)
        if action == 'update_appointment_date':
            return JsonResponse(response, safe=False)
        back_url = response['back_url']
        return redirect(back_url)


class PatientDetailView(TemplateView):
    template_name = 'patient/detail.html'

    def get_context_data(self, pk, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=pk)
        context['last_order'] = Order.objects.filter(status=True).order_by('-id').first()
        context['doctors'] = User.objects.filter(status='active', role__in=['doctor', 'admin'])
        context['orders'] = Order.objects.select_related('doctor', 'registrar').filter(patient_id=pk)
        return context


class PatientListView(TemplateView):
    template_name = 'patient/list.html'

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        return context


class PatientUpdateView(UpdateView):
    template_name = 'patient/update.html'
    model = Patient
    fields = ['fullname', 'phone', 'address', 'birthday', 'doc_type', 'doc_series', 'doc_number', 'status', 'registrar']

    def get_success_url(self):
        return reverse('patient_list')


class AppointmentListView(TemplateView):
    template_name = 'appointment/list.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        role = self.request.user.role
        filter_date = self.request.GET.get('filter_date')
        filter_dict = {}
        if role == 'doctor':
            filter_dict['doctor_id'] = self.request.user.id
        if filter_date:
            filter_dict['created__date'] = filter_date
        context['appointments'] = Appointment.objects.filter(**filter_dict).order_by('appointment_date', '-sent')
        context['patients'] = Patient.objects.all()
        context['doctors'] = User.objects.filter(role__in=['doctor', 'admin'])
        return context


class MyAppointmentListView(TemplateView):
    template_name = 'appointment/list.html'

    def get_context_data(self, **kwargs):
        context = super(MyAppointmentListView, self).get_context_data(**kwargs)
        filter_date = self.request.GET.get('filter_date')
        filter_dict = {'doctor_id': self.request.user.id}
        if filter_date:
            filter_dict['created__date'] = filter_date
        context['appointment'] = Appointment.objects.filter(**filter_dict).order_by('appointment_date', '-sent')
        context['patients'] = Patient.objects.all()
        context['doctors'] = User.objects.filter(role__in=['doctor', 'admin'])
        context['send_tg_to_patients'] = True
        return context


class AppointmentUpdateView(UpdateView):
    template_name = 'appointment/update.html'
    model = Appointment
    fields = ['patient', 'doctor', 'appointment_date']

    def get_success_url(self):
        return reverse('appointment_list')

    def get_initial(self):
        initial = super(AppointmentUpdateView, self).get_initial()
        initial['date'] = self.model.objects.get(id=self.kwargs['pk']).date.strftime('%Y-%m-%dT%H:%M:%S')
        return initial
