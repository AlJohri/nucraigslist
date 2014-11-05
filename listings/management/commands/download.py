from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        import os, sys
        from dateutil.parser import parse
        from facebook import GraphAPI, GraphAPIError
        from socialscraper.facebook.graphapi import get_feed
        FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
        api = GraphAPI(FACEBOOK_USER_TOKEN)

        try:
            api.get_object('me')
        except GraphAPIError as e:
            print e
            print "Update and source your .secret file"
            sys.exit()

        for item in get_feed(api, "357858834261047", start=parse("10-1-2014"), end=parse("11-1-2014")):
            print "-----------------------------------------------------"
            print item['id'], item['created_time'], item['updated_time'], item['message'], item        
            if 'comments' in item:
                comments = api.get_object("/" + item['id'] + '/comments')
                comments = comments['data']
                print ([comment['message'] for comment in comments])
            item['_id'] = item['id']
            del item['id']

        #     try:
        #         poll = Poll.objects.get(pk=int(poll_id))
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write('Successfully closed poll "%s"' % poll_id)