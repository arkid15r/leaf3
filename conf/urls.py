"""Project URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.core import views as core_views

urlpatterns = [
    path('', core_views.Main.as_view(), name='main'),
    path('', include('apps.tree.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.schema.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ALL_AUTH_URL, include('allauth.urls')),
]
