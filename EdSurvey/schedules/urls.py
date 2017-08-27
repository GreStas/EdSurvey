from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^schedule$', views.schedule_index, name='schedule'),
    url(r'^task$', views.task_index, name='task'),
    # url(r'^schedule/(?P<scheduleid>\d+)$', views.schedule_info, name='scheduleinfo'),
    # url(r'^newattempt/(?P<scheduleid>\d+)$', views.new_attempt, name='newattempt'),
    # url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
]