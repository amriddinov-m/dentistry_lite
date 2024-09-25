from django.urls import path
from rest_framework import routers

from patient.api_views import PatientView
from patient.views import PatientActionView, PatientDetailView, PatientListView, PatientUpdateView, AppointmentListView, \
    AppointmentActionView, AppointmentUpdateView, MyAppointmentListView
from user.views import send_sms, send_notification

router = routers.SimpleRouter()
router.register('api/v1/patients', PatientView, basename='patient_list')

urlpatterns = [
    path('patient/action/', PatientActionView.as_view(), name='patient_action'),
    path('patient/list/', PatientListView.as_view(), name='patient_list'),
    path('patient/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('appointment/action/', AppointmentActionView.as_view(), name='appointment_action'),
    path('appointment/list/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/my/', MyAppointmentListView.as_view(), name='my_appointment_list'),
    path('appointment/send/<int:pk>', send_notification, name='send_notification'),
    path('appointment/update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('bot/send/', send_sms),
]
