from django.conf.urls import url
from listings import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail'),
]