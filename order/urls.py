from django.urls import path
from django.views.generic.base import TemplateView

from order.views import OrderListView, OrderDetailView, OrderActionView, OrderUpdateView, OrderPrintView, \
    OrderReportView

urlpatterns = [
    path('order/action/', OrderActionView.as_view(), name='order_action'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('order/print/<int:pk>/', OrderPrintView.as_view(), name='order_print'),
    path('order/report/<int:pk>', OrderReportView.as_view(), name='order_report'),

]
