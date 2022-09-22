from django.urls import reverse

from order.models import Order, OrderItem


def create_order(post_request, user):
    patient_id = post_request.get('patient')
    doctor_id = post_request.get('doctor')
    content = post_request.get('content')
    diagnosis = post_request.get('diagnosis')
    order = Order.objects.create(patient_id=patient_id, doctor_id=doctor_id, content=content, registrar=user, diagnosis=diagnosis)
    return dict({'back_url': reverse('order_detail', kwargs={'pk': order.pk}),
                 'data': ''})


def create_order_for_patient(post_request, user):
    patient_id = post_request.get('patient_id')
    doctor_id = post_request.get('doctor')
    content = post_request.get('content')
    order = Order.objects.create(patient_id=patient_id, doctor_id=doctor_id, content=content, registrar=user)
    return dict({'back_url': reverse('order_detail', kwargs={'pk': order.pk}),
                 'data': ''})


def create_order_item(post_request, user):
    order_id = post_request.get('order_id')
    service_id = post_request.get('service_id')
    price = post_request.get('price')
    count = post_request.get('count')
    total = post_request.get('total')
    tooth = post_request.get('tooth')
    content = post_request.get('content')
    OrderItem.objects.create(service_id=service_id, order_id=order_id, price=price, count=count, amount=total,
                             tooth=tooth, content=content, registrar=user)
    return dict({'back_url': reverse('order_detail', kwargs={'pk': order_id}),
                 'data': ''})


def update_status_order(post_request, user):
    order_id = post_request.get('order_id')
    status = post_request.get('status')
    if (post_request.get('inspection')):
        inspection = post_request.get('inspection')
        Order.objects.filter(id=order_id).update(status=status, inspection=inspection)
    else:
        Order.objects.filter(id=order_id).update(status=status)

    return dict({'back_url': reverse('order_detail', kwargs={'pk': order_id}),
                 'data': ''})


def delete_order(post_request, user):
    order_id = post_request.get('order_id')
    Order.objects.get(id=order_id).delete()
    return dict({'back_url': reverse('order_list'),
                 'data': ''})


def delete_order_item(post_request, user):
    order_id = post_request.get('order_id')
    item_id = post_request.get('item_id')
    OrderItem.objects.get(id=item_id).delete()
    return dict({'back_url': reverse('order_detail', kwargs={'pk': order_id}),
                 'data': ''})
