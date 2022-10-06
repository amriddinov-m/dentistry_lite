from django.urls import path
from rest_framework import routers

from patient.api_views import PatientView
from patient.views import PatientActionView, PatientDetailView, PatientListView, PatientUpdateView, RecordListView, \
    RecordActionView, RecordUpdateView, MyRecordListView
from user.views import send_sms, send_notification

router = routers.SimpleRouter()
router.register('api/v1/patients', PatientView)

urlpatterns = [
    path('patient/action/', PatientActionView.as_view(), name='patient_action'),
    path('patient/list/', PatientListView.as_view(), name='patient_list'),
    path('patient/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('record/action/', RecordActionView.as_view(), name='record_action'),
    path('record/list/', RecordListView.as_view(), name='record_list'),
    path('record/my/', MyRecordListView.as_view(), name='my_record_list'),
    path('record/send/<int:pk>', send_notification, name='send_notification'),
    path('record/update/<int:pk>/', RecordUpdateView.as_view(), name='record_update'),
    path('bot/send/', send_sms),
]
