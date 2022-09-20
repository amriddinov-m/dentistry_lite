import datetime

from patient.models import Patient, Record
from user.models import User


def pages(request):
    datetime_now = datetime.datetime.now()
    return {
        'patients': Patient.objects.filter(status='active'),
        'doctors': User.objects.filter(role='doctor'),
        'records_today': Record.objects.filter(date__year=datetime_now.year,
                                               date__month=datetime_now.month,
                                               date__day=datetime_now.day)
    }
