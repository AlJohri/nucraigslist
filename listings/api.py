from tastypie.resources import ModelResource
from tastypie import fields
from listings.models import Listing, User, Comment, Group

class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'group'

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class CommentResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    #listing = fields.ToOneField(ListingResource, 'listing' ,full=True)

   #bundle.data['commentId'] = bundle.data['comment'].data['id']
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'

class ListingResource(ModelResource):
    group = fields.ToOneField(GroupResource, 'group', full=True)
    user = fields.ToOneField(UserResource, 'user', full=True)
    comments = fields.ToManyField(CommentResource, 'comments', full=True, full_list=False, full_detail=True, null=True)
    likers = fields.ToManyField(UserResource, 'likers', full=True, null=True)

    def dehydrate(self, bundle):
        bundle.data['user_id'] = bundle.data['user'].data['id']
        bundle.data['group_id'] = bundle.data['group'].data['id']
        return bundle

    class Meta:
        queryset = Listing.objects.exclude(message="")
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



