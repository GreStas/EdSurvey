from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^scheduleinfo/(?P<scheduleid>\d+)$', views.schedule_info, name='scheduleinfo'),
    url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
    url(r'^newattempt/(?P<scheduleid>\d+)$', views.new_attempt, name='newattempt'),
]