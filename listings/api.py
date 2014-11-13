from tastypie.resources import ModelResource
from tastypie import fields
from listings.models import Listing, User, Comment


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'seller'

class CommentResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    #listing = fields.ToOneField(ListingResource, 'listing' ,full=True)

   #bundle.data['commentId'] = bundle.data['comment'].data['id']
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'

class ListingResource(ModelResource):
    seller = fields.ToOneField(UserResource, 'seller', full=True)
    comment = fields.ToManyField(CommentResource, 'comment', full=True, null=True)
    def dehydrate(self, bundle):
        bundle.data['sellerId'] = bundle.data['seller'].data['id']
        return bundle

    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        # authentication = Authentication()
        # authorization = Authorization()
        always_return_data = True
        filtering = {
            "buy_or_sell": ('exact',),
            "category": ('exact',),
            "message": ('icontains',),
        }
        ordering = ['updated_time', 'created_time']



