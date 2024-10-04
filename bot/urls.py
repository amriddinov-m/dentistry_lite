from django.urls import path

from bot.views import HomePageView, UserProfileView, CreateAppointmentView, UserUpdateView

urlpatterns = [
    path('home-page/', HomePageView.as_view(), name='home-page'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-update/', UserUpdateView.as_view(), name='user-update'),
    path('create-appointment/', CreateAppointmentView.as_view(), name='create-appointment'),
]
