from django.urls import path

from patient.views import PatientActionView, PatientDetailView, PatientListView, PatientUpdateView, RecordListView, \
    RecordActionView, RecordUpdateView

urlpatterns = [
    path('patient/action/', PatientActionView.as_view(), name='patient_action'),
    path('patient/list/', PatientListView.as_view(), name='patient_list'),
    path('patient/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('record/action/', RecordActionView.as_view(), name='record_action'),
    path('record/list/', RecordListView.as_view(), name='record_list'),
    path('record/update/<int:pk>/', RecordUpdateView.as_view(), name='record_update'),
]
