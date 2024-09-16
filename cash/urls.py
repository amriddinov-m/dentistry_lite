from django.urls import path

from cash.views import CashListView, CashActionView, CashLogListView

urlpatterns = [
    path('cash/action/', CashActionView.as_view(), name='cash_action'),
    path('cash/list/', CashListView.as_view(), name='cash_list'),
    path('cash/log/list/', CashLogListView.as_view(), name='cash_log_list'),
]
