from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url


urlpatterns = [
    path('', include('pages.urls')),
]
