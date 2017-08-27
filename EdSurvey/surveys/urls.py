from django.conf.urls import url
from . import views
import surveys

urlpatterns = [
    url(r'^$', views.index),
    url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
    url(r'^showquery/(?P<queryid>\d+)$', surveys.views.show_query, name='showquery'),
    url(r'^finishattempt/(?P<attemptid>\d+)$', views.finish_attempt, name='finishattempt'),
    url(r'^closeattempt/(?P<attemptid>\d+)$', views.close_attempt, name='closeattempt'),
    url(r'^scheduleinfo/(?P<scheduleid>\d+)$', views.schedule_info, name='scheduleinfo'),
    url(r'^newattempt/(?P<scheduleid>\d+)$', views.new_attempt, name='newattempt'),
]