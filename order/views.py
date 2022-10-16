from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView

import order
from order.logic import create_order, create_order_item, update_status_order, delete_order, create_order_for_patient, \
    delete_order_item
from order.models import Order, OrderItem

from patient.models import Patient
from service.models import Service, ServiceCategory
from user.models import User


class OrderActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        print(post_request)
        user = self.request.user
        action = self.request.POST.get('action', None)
        print(action)
        actions = {
            'create_order': create_order,
            'create_order_for_patient': create_order_for_patient,
            'create_order_item': create_order_item,
            'update_status_order': update_status_order,
            'delete_order': delete_order,
            'delete_order_item': delete_order_item,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        return redirect(back_url)


class OrderListView(TemplateView):
    template_name = 'order/list.html'

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        role = self.request.user.role
        filter_date = self.request.GET.get('filter_date')
        print(filter_date)
        filter_dict = {}
        if role == 'doctor':
            filter_dict['doctor_id'] = self.request.user.id
        if filter_date:
            filter_dict['created__date'] = filter_date
        context['filter_date'] = filter_date
        context['orders'] = Order.objects.filter(**filter_dict)
        context['redirect_url'] = 'order_list'
        context['patients'] = Patient.objects.filter(status='active')
        context['doctors'] = User.objects.filter(status='active', role__in=['doctor', 'admin'])
        return context


class MyOrderListView(TemplateView):
    template_name = 'order/list.html'

    def get_context_data(self, **kwargs):
        context = super(MyOrderListView, self).get_context_data(**kwargs)
        filter_date = self.request.GET.get('filter_date')
        filter_dict = {'doctor_id': self.request.user.id}
        if filter_date:
            filter_dict['created__date'] = filter_date

        context['filter_date'] = filter_date
        context['redirect_url'] = 'my_order_list'
        context['orders'] = Order.objects.filter(**filter_dict)
        context['patients'] = Patient.objects.filter(status='active')
        context['doctors'] = User.objects.filter(status='active', role__in=['doctor', 'admin'])
        return context


class OrderDetailView(TemplateView):
    template_name = 'order/detail.html'

    def get_context_data(self, pk, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order=pk)
        context['order'] = Order.objects.get(id=pk)
        context['order_items'] = order_items
        context['categories'] = ServiceCategory.objects.filter(status='active')
        context['services'] = Service.objects.filter(status='active')
        context['total_amount'] = order_items.aggregate(total=Sum('amount'))['total'] or 0
        return context


class OrderReportView(TemplateView):
    template_name = 'order/report.html'

    def get_context_data(self, pk, **kwargs):
        context = super(OrderReportView, self).get_context_data(**kwargs)
        tooth = self.request.GET.get('tooth')
        order_items = OrderItem.objects.filter(tooth=tooth, order__status='done', order__patient_id=pk)
        context['order_items'] = order_items
        context['patient'] = Patient.objects.get(pk=pk)
        context['tooth'] = tooth
        context['total_amount'] = order_items.aggregate(total=Sum('amount'))['total'] or 0
        return context


class OrderPrintView(TemplateView):
    template_name = 'order/print.html'

    def get_context_data(self, pk, **kwargs):
        context = super(OrderPrintView, self).get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order=pk)
        context['order'] = Order.objects.get(id=pk)
        context['order_items'] = order_items
        context['total_amount'] = order_items.aggregate(total=Sum('amount'))['total'] or 0

        return context


class OrderUpdateView(UpdateView):
    template_name = 'order/update.html'
    model = Order
    fields = ['patient', 'doctor', 'content']

    def get_success_url(self):
        back_url = self.request.GET.get('back_url')
        back_pk = self.request.GET.get('back_pk')
        if back_pk:
            return reverse(back_url, kwargs={'pk': back_pk})
        return reverse(back_url)
