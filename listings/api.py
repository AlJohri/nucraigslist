from tastypie.resources import ModelResource
from tastypie import fields
from listings.models import Listing, User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'seller'


class ListingResource(ModelResource):
    seller = fields.ForeignKey(UserResource, 'seller')
    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        # authentication = Authentication()
        # authorization = Authorization()
        always_return_data = True

