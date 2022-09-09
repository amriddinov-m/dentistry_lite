from django.urls import path

from service.views import ServiceCategoryListView, ServiceActionView, ServiceCategoryDetailView

urlpatterns = [
    path('service/action/', ServiceActionView.as_view(), name='service_action'),
    path('service/category/list/', ServiceCategoryListView.as_view(), name='service_category_list'),
    path('service/category/detail/<int:pk>/', ServiceCategoryDetailView.as_view(), name='service_category_detail'),
]
