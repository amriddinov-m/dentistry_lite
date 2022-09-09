from django.urls import reverse

from service.models import ServiceCategory, Service


def create_service_category(post_request, user):
    name = post_request.get('name')
    status = post_request.get('status')
    ServiceCategory.objects.create(name=name, status=status)
    return dict({'back_url': reverse('service_category_list'),
                 'data': ''})


def delete_service_category(post_request, user):
    category_id = post_request.get('category_id')
    ServiceCategory.objects.filter(id=category_id).delete()
    return dict({'back_url': reverse('service_category_list'),
                 'data': ''})


def update_service_category(post_request, user):
    category_id = post_request.get('category_id')
    name = post_request.get('name')
    status = post_request.get('status')
    ServiceCategory.objects.filter(id=category_id).update(name=name, status=status)
    return dict({'back_url': reverse('service_category_list'),
                 'data': ''})


def create_service(post_request, user):
    category_id = post_request.get('category_id')
    name = post_request.get('name')
    price = post_request.get('price')
    status = post_request.get('status')
    Service.objects.create(name=name, price=price, category_id=category_id, status=status)
    return dict({'back_url': reverse('service_category_detail', kwargs={'pk': category_id}),
                 'data': ''})


def delete_service(post_request, user):
    category_id = post_request.get('category_id')
    service_id = post_request.get('service_id')
    Service.objects.filter(id=service_id).delete()
    return dict({'back_url': reverse('service_category_detail', kwargs={'pk': category_id}),
                 'data': ''})


def update_service(post_request, user):
    category_id = post_request.get('category_id')
    service_id = post_request.get('service_id')
    name = post_request.get('name')
    price = post_request.get('price')
    status = post_request.get('status')
    Service.objects.filter(id=service_id).update(name=name, price=price, status=status)
    return dict({'back_url': reverse('service_category_detail', kwargs={'pk': category_id}),
                 'data': ''})
