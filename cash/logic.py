from django.urls import reverse

from cash.models import Cash


def create_cash(post_request, user):
    name = post_request.get('name')
    amount = post_request.get('amount')
    status = post_request.get('status')
    method = post_request.get('method')
    Cash.objects.create(name=name, amount=amount, method=method, status=status, creator=user)
    return dict({'back_url': reverse('cash_list'),
                 'data': ''})


def delete_cash(post_request, user):
    cash_id = post_request.get('cash_id')
    Cash.objects.filter(id=cash_id).delete()
    return dict({'back_url': reverse('cash_list'),
                 'data': ''})


def update_cash(post_request, user):
    cash_id = post_request.get('cash_id')
    name = post_request.get('name')
    amount = post_request.get('amount')
    status = post_request.get('status')
    method = post_request.get('method')
    Cash.objects.filter(id=cash_id).update(name=name, amount=amount, method=method, status=status)
    return dict({'back_url': reverse('cash_list'),
                 'data': ''})
