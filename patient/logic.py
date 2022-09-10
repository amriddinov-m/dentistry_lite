from django.urls import reverse

from patient.models import Patient, Record


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
    doc_type = post_request.get('doc_type')
    doc_series = post_request.get('doc_series')
    doc_number = post_request.get('doc_number')
    image = post_request.get('image')
    patient = Patient.objects.create(fullname=fullname, birthday=birthday, last_visit=last_visit, address=address,
                                     phone=phone, doc_type=doc_type, doc_series=doc_series, doc_number=doc_number,
                                     image=image, registrar=user)
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
