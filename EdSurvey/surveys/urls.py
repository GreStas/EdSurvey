from django.conf.urls import url, include
from . import views
import surveys

urlpatterns = [
    url(r'^$', views.index),
    url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
    url(r'^showquery/(?P<queryid>\d+)$', surveys.views.show_query, name='showquery'),
    url(r'^finishattempt/(?P<attemptid>\d+)$', views.finish_attempt, name='finishattempt'),
    url(r'^closeattempt/(?P<attemptid>\d+)$', views.close_attempt, name='closeattempt'),
 ]