from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from listings.api import ListingResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ListingResource())

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    (r'^', include('listings.urls', namespace='listings')),
)
