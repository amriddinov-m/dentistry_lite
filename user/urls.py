from django.urls import path
from django.views.generic.base import TemplateView

from user.views import HomeView, LoginView, DoctorListView, DoctorUpdateView, DoctorActionView, \
    DoctorCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('doctor/action/', DoctorActionView.as_view(), name='doctor_action'),
    path('doctor/list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('login/', LoginView.as_view(), name="login-view"),
    path(".well-known/pki-validation/148A1FAF6AB3ECC87BFB13A95A6A1BA3.txt",
         TemplateView.as_view(template_name="ssl_files.html", content_type="text/plain")),

]
