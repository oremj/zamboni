from optparse import make_option

from django.core.management.base import BaseCommand

import amo
from files.models import File

HELP = 'List all marketplace packaged apps'


statuses = {'pending': amo.STATUS_NOMINATED,
            'public': amo.STATUS_PUBLIC,
            'approved': amo.STATUS_PUBLIC_WAITING}


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--status',
                    default='public',
                    choices=statuses.keys(),
                    help='Should be one of (pending, public, approved)')
        )

    help = HELP

    def handle(self, *args, **kwargs):
        status = statuses[kwargs['status']]
        files = []
        for f in File.objects.filter(version__addon__type=11,
                                     version__addon__status=status,
                                     version__addon__is_packaged=True):
            try:
                files.append(f.file_path)
            except:
                pass
        print "\n".join(files)
