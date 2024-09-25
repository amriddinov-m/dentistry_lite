import datetime

import requests
from django.urls import reverse
from patient.models import Patient, Appointment

BOT_TOKEN = '5572492160:AAEL_pd6CsZ5ZSo2rAUkOWX9H-iTo8wamV4'


def create_appointment(post_request, user):
    appointment_type = post_request.get('appointment_type')
    doctor_id = post_request.get('doctor')
    appointment_date = post_request.get('appointment_date')
    appointment_time = post_request.get('appointment_time')
    duration = post_request.get('duration')
    patient_id = post_request.get('patient')
    description = post_request.get('patient')
    appointment_datetime = f'{appointment_date}T{appointment_time}'
    Appointment.objects.create(appointment_type=appointment_type, doctor_id=doctor_id,
                               appointment_date=appointment_datetime, duration=duration, patient_id=patient_id,
                               description=description, creator=user)
    return dict({'back_url': reverse('home-view'),
                 'data': ''})


def update_appointment_date(post_request, user):
    results = {'status': 200}
    appointment_id = post_request.get('appointment_id')
    appointment_date = post_request.get('appointment_date')
    duration = post_request.get('duration')
    Appointment.objects.filter(id=appointment_id).update(appointment_date=appointment_date, duration=duration)
    return results

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
    Patient.objects.filter(id=patient_id).delete()

    return dict({'back_url': reverse('patient_list'),
                 'data': ''})


def delete_appointment(post_request, user):
    appointment_id = post_request.get('appointment_id')
    Appointment.objects.filter(id=appointment_id).delete()
    return dict({'back_url': reverse('appointment_list'),
                 'data': ''})


def get_appointments(post_request, user):
    datetime_now = datetime.datetime.now()
    results = []
    appointments = Appointment.objects.filter(date__year=datetime_now.year,
                                              date__month=datetime_now.month,
                                              date__day=datetime_now.day,
                                              sent=False)
    for appointment in appointments:
        results.append({
            'id': appointment.id,
            'date': appointment.date.strftime("%H:%M")
        })
    return dict({
        'back_url': reverse(post_request.get('back_url')),
        'results': results
    })


def send_sms_today_patients(post_request, user):
    datetime_now = datetime.datetime.now()
    user_id = post_request.get('user_id')
    appointments = Appointment.objects.filter(date__year=datetime_now.year,
                                              date__month=datetime_now.month,
                                              date__day=datetime_now.day,
                                              doctor_id=user_id,
                                              patient__chat_id__isnull=False)
    for appointment in appointments:
        if appointment.patient.gender == 'male':
            gender_text = 'Уважаемый'
        else:
            gender_text = 'Уважаемая'
        text = f'{gender_text}, {appointment.patient.fullname}\n\n' \
               f'🕘 Напоминаем вам, что вы записаны сегодня в {appointment.date.strftime("%Y-%m-%d %H:%M")}\n' \
               f'🦷 На прием к стоматологу {appointment.doctor.fullname} \n\n' \
               f'👨🏻‍⚕ Администратор клиники "Центр ортодонтии"\n\n' \
               f'📞 +998(98) 273-52-00\n'
        data = {
            'chat_id': appointment.patient.chat_id,
            'text': text
        }
        location_data = {
            'chat_id': appointment.patient.chat_id,
            'latitude': '39.662252',
            'longitude': '66.941450',
        }
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        location_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendLocation'

        requests.post(url, data)
        requests.post(location_url, location_data)
        appointment.sent = True
        appointment.save()
    return dict({'back_url': reverse('my_appointment_list'),
                 'data': ''})
