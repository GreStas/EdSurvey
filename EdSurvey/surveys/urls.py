from django.conf.urls import url, include
from . import views
import surveys

urlpatterns = [
    url(r'^$', views.index),
    url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
    url(r'^showquery/(?P<queryid>\d+)$', surveys.views.show_query, name='showquery'),
    url(r'^finishattempt/(?P<attemptid>\d+)$', views.finish_attempt, name='finishattempt'),
    # url(r'^choicerun/$', views.choice_run),
    # url(r'^choicedone/$', views.choice_done),
    # url(r'^choiceattempt/(?P<scheduleid>\d+)$', views.choice_attempt),
 ]