import datetime
import requests
from django.urls import reverse

from patient.models import Patient, Record

BOT_TOKEN = '5572492160:AAEL_pd6CsZ5ZSo2rAUkOWX9H-iTo8wamV4'


def create_record(post_request, user):
    patient_id = post_request.get('patient_id')
    doctor_id = post_request.get('doctor_id')
    date = post_request.get('date')
    content = post_request.get('content')
    Record.objects.create(patient_id=patient_id, doctor_id=doctor_id, date=date, content=content, registrar=user)
    return dict({'back_url': reverse('record_list'),
                 'data': ''})


def create_patient(post_request, user):
    fullname = post_request.get('fullname')
    birthday = post_request.get('birthday')
    last_visit = post_request.get('last_visit')
    address = post_request.get('address')
    phone = post_request.get('phone')
    gender = post_request.get('gender')
    doc_type = post_request.get('doc_type')
    doc_series = post_request.get('doc_series')
    doc_number = post_request.get('doc_number')
    image = post_request.get('image')
    patient = Patient.objects.create(fullname=fullname, birthday=birthday, last_visit=last_visit, address=address,
                                     phone=phone, doc_type=doc_type, doc_series=doc_series, doc_number=doc_number,
                                     image=image, registrar=user, gender=gender)
    return dict({'back_url': reverse('patient_detail', kwargs={'pk': patient.pk}),
                 'data': ''})


def delete_patient(post_request, user):
    patient_id = post_request.get('patient_id')
    print(patient_id)
    Patient.objects.filter(id=patient_id).delete()

    return dict({'back_url': reverse('patient_list'),
                 'data': ''})


def delete_record(post_request, user):
    record_id = post_request.get('record_id')
    Record.objects.filter(id=record_id).delete()
    return dict({'back_url': reverse('record_list'),
                 'data': ''})


def get_records(post_request, user):
    datetime_now = datetime.datetime.now()
    results = []
    records = Record.objects.filter(date__year=datetime_now.year,
                                    date__month=datetime_now.month,
                                    date__day=datetime_now.day,
                                    sent=False)
    for record in records:
        results.append({
            'id': record.id,
            'date': record.date.strftime("%H:%M")
        })
    return dict({
        'back_url': reverse(post_request.get('back_url')),
        'results': results
    })


def send_message_to_tg(post_request, user):
    record_id = post_request.get('record_id')
    record = Record.objects.get(id=record_id)
    if record.patient.gender == 'male':
        gender_text = 'Уважаемый'
    else:
        gender_text = 'Уважаемая'
    text = f'{gender_text} {record.patient.fullname}\n' \
           f'Напоминаем вам что, у вас назначен визит к стоматологу {record.doctor.fullname}\n' \
           f'🦷 В клинику "Центр ортодонтии"\n' \
           f'🕘 Назначенное время: {record.date.strftime("%Y-%m-%d %H:%M")}\n' \
           f'❗️Просим вас прибыть в назаначенное время.'
    data = {
        'chat_id': record.patient.chat_id,
        'text': text
    }
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    requests.post(url, data)
    record.sent = True
    record.save()
    return dict({
        'back_url': reverse(post_request.get('back_url')),
        'data': ''
    })
