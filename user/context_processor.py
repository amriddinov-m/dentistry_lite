import datetime

from patient.models import Patient, Record
from user.models import User
from django.core.exceptions import PermissionDenied


def pages(request):
    datetime_now = datetime.datetime.now()
    data = {
        'patients': Patient.objects.filter(status='active'),
        'doctors': User.objects.filter(role__in=['doctor', 'admin']),
        'records_today': Record.objects.filter(date__year=datetime_now.year,
                                               date__month=datetime_now.month,
                                               date__day=datetime_now.day)
    }

    path = request.path
    if request.user.is_authenticated:
        role = request.user.role
        if request.user.is_superuser or role == 'admin':
            return data

        elif role == 'registrar':
            if path == '/service/action/' or path == '/service/category/list/' \
                    or path.startswith('/service/category/detail/') or path == '/doctor/action/' \
                    or path == '/doctor/list/' or path == '/doctor/create/' or path.startswith('/doctor/update/'):
                raise PermissionDenied

        elif role == 'doctor':
            if path == '/patient/action/' or path == '/patient/list/' or path.startswith('/patient/detail/') \
                    or path.startswith('/patient/update/') or path == '/service/action/' \
                    or path == '/service/category/list/' or path.startswith('/service/category/detail/') \
                    or path == '/doctor/action/' or path == '/doctor/list/' or path == '/doctor/create/' \
                    or path.startswith('/doctor/update/'):
                raise PermissionDenied

    return data
