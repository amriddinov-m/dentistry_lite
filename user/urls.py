from django.urls import path
from user.views import HomeView, LoginView, DoctorListView, DoctorUpdateView, DoctorActionView, \
    DoctorCreateView, SslFiles

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('doctor/action/', DoctorActionView.as_view(), name='doctor_action'),
    path('doctor/list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('login/', LoginView.as_view(), name="login-view"),
]
