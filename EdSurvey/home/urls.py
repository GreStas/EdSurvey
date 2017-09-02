from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^contacts$', views.contacts, name='contacts'),
    url(r'^manuals$', views.manuals, name='manuals'),
]