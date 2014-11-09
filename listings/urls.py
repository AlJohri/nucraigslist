from django.conf.urls import *
from listings import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail')
)