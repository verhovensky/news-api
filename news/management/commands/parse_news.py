from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Parse news from Yandex and Ozon'

    # def add_arguments(self, parser):
    #     parser.add_argument('verbose', nargs='+', type=bool)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Post.objects.get(pk=poll_id)
            except Post.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))