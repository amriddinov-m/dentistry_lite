"""dentistry_light URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from dentistry_light import settings
from dentistry_light.router import DefaultRouter
from patient.urls import router as patient_router
from user.views import LoginView, custom_logout

router = DefaultRouter()
router.extend(patient_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include(router.urls)),
    path('i18n/', include('django.conf.urls.i18n')),
    path('login/', LoginView.as_view(), name="login-view"),
    path('logout/', custom_logout, name="logout"),
    path('webapp/', include('bot.urls')),

]

urlpatterns += i18n_patterns(
    path('', include('order.urls')),
    path('', include('patient.urls')),
    path('', include('service.urls')),
    path('', include('user.urls')),
    path('', include('cash.urls')),
)

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
