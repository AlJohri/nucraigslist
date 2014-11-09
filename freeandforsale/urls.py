from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from listings.api import ListingResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ListingResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freeandforsale.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^listings/', include('listings.urls', namespace='listings')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls))
)
