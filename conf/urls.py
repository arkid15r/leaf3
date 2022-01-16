"""Project URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.core.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ALL_AUTH_URL, include('allauth.urls')),
]
