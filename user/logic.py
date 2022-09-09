from django.urls import reverse

from user.models import User


def update_status_doctor(post_request, user):
    doctor_id = post_request.get('doctor_id')
    status = post_request.get('status')
    User.objects.filter(id=doctor_id).update(status=status)
    return dict({'back_url': reverse('order_detail', kwargs={'pk': doctor_id}),
                 'data': ''})


def delete_doctor(post_request, user):
    doctor_id = post_request.get('doctor_id')
    User.objects.get(id=doctor_id).delete()
    return dict({'back_url': reverse('doctor_list'),
                 'data': ''})
