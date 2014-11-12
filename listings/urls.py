from django.conf.urls import *
from listings import views

urlpatterns = patterns('',
	url(r'^.*', views.index, name='index')
)