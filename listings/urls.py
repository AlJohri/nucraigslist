from django.conf.urls import *
from listings import views
from tastypie.api import Api
from listings.api import ListingResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ListingResource())

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^api/', include(v1_api.urls)),
)