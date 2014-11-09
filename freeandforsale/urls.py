from django.conf.urls import patterns, include, url
from django.contrib import admin

from listings.api import ListingResource
listing_resource = ListingResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freeandforsale.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^listings/', include('listings.urls', namespace='listings')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(listing_resource.urls))
)
