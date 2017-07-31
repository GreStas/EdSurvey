from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^runattempt/(?P<attemptid>\d+)$', views.run_attempt, name='runattempt'),
    url(r'^showquery/(?P<queryid>\d+)$', views.show_query, name='showquery'),
    # url(r'^choicerun/$', views.choice_run),
    # url(r'^choicedone/$', views.choice_done),
    # url(r'^choiceattempt/(?P<scheduleid>\d+)$', views.choice_attempt),
 ]