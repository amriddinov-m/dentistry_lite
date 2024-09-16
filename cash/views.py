from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from cash.logic import create_cash, delete_cash, update_cash
from cash.models import Cash, CashLog
from patient.models import Patient
from service.models import Service


class CashActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CashActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user = self.request.user
        action = self.request.POST.get('action', None)
        print(action)
        actions = {
            'create_cash': create_cash,
            'delete_cash': delete_cash,
            'update_cash': update_cash,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        return redirect(back_url)


class CashListView(TemplateView):
    template_name = 'cash/list.html'

    def get_context_data(self, **kwargs):
        context = super(CashListView, self).get_context_data(**kwargs)
        context['cashes'] = Cash.objects.order_by('id')
        return context


class CashLogListView(TemplateView):
    template_name = 'cash/log_list.html'

    def get_context_data(self, **kwargs):
        context = super(CashLogListView, self).get_context_data(**kwargs)
        context['cash_logs'] = CashLog.objects.order_by('-created')
        context['cashes'] = Cash.objects.order_by('id')
        context['patients'] = Patient.objects.filter(status='active')
        context['services'] = Service.objects.filter(status='active')
        return context
