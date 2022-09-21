from django.urls import path
from django.views.generic.base import TemplateView

from order.views import OrderListView, OrderDetailView, OrderActionView, OrderUpdateView

urlpatterns = [
    path('order/action/', OrderActionView.as_view(), name='order_action'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
]
