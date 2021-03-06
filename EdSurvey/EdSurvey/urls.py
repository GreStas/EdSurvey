"""EdSurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from home.views import index as homepage
from clients.views import log_in, log_out

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homepage, name='homepage'),
    url(r'^login$', log_in, name='login'),
    url(r'^logout$', log_out, name='logout'),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^questions/', include('questions.urls', namespace='questions')),
    url(r'^querylists/', include('querylists.urls', namespace='querylists')),
    url(r'^schedules/', include('schedules.urls', namespace='schedules')),
    url(r'^surveys/', include('surveys.urls', namespace='surveys')),
    url(r'^clients/', include('clients.urls', namespace='clients')),
]
