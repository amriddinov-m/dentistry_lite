from django.urls import path
from user.views import HomeView, DoctorListView, DoctorUpdateView, DoctorActionView, \
    DoctorCreateView, SslFiles, WebAppView

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('doctor/action/', DoctorActionView.as_view(), name='doctor_action'),
    path('doctor/list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('web-app/', WebAppView.as_view(), name="web-app"),
    path(".well-known/pki-validation/506A87593918CABE2A944065C5E7B9E9.txt", SslFiles.as_view()),

]
