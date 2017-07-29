from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^scheduleinfo/(?P<scheduleid>\d+)$', views.schedule_info, name='scheduleinfo'),
 ]