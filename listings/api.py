from tastypie.resources import ModelResource
from listings.models import Listing

class ListingResource(ModelResource):
    """
    API Facet
    """
    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        # authentication = Authentication()
        # authorization = Authorization()
        always_return_data = True

