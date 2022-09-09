from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from service.logic import create_service_category, delete_service_category, update_service_category, create_service, \
    delete_service, update_service
from service.models import ServiceCategory, Service


class ServiceCategoryListView(TemplateView):
    template_name = 'service/list.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoryListView, self).get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context


class ServiceCategoryDetailView(TemplateView):
    template_name = 'service/detail.html'

    def get_context_data(self, pk, **kwargs):
        context = super(ServiceCategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = ServiceCategory.objects.get(id=pk)
        context['services'] = Service.objects.filter(category_id=pk)
        return context


class ServiceActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ServiceActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user = self.request.user
        action = self.request.POST.get('action', None)
        print(action)
        actions = {
            'create_service_category': create_service_category,
            'delete_service_category': delete_service_category,
            'update_service_category': update_service_category,
            'create_service': create_service,
            'delete_service': delete_service,
            'update_service': update_service,
        }
        response = actions[action](post_request, user)
        back_url = response['back_url']
        return redirect(back_url)
