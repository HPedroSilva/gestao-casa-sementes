"""sementesaefa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from distutils.log import debug
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from mainApp.views import DashboardView
from django.contrib.auth.decorators import login_required
import notifications.urls

admin.site.site_header = "Casa de Sementes - Admin"
admin.site.site_title = "Casa de Sementes - Admin"
admin.site.index_title = "Casa de Sementes - Admin"

urlpatterns = [
    path('', login_required(DashboardView.as_view()), name='index'),
    path('admin/', admin.site.urls),
    path('dynamic-admin-form/', include('dynamic_admin_forms.urls')),
    path('mainapp/', include('mainApp.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
