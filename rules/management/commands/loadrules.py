import os
from django.core.management.base import BaseCommand
from django.conf import settings

from rules.models import get_rules, load_rules


class Command(BaseCommand):
    help = "Rules file loader"

    def handle(self, *args, **options):
        filename = input("Enter templates file to be loaded (hit enter for valacdos.txt in MEDIA_ROOT): ")
        if not filename:
            filename = os.path.join(settings.MEDIA_ROOT, 'valacdos.txt')
        rows = get_rules(filename)
        if rows is None:
            self.stdout.write('File %s not found' % filename)
            return
        records = load_rules(rows)
        self.stdout.write("Records Loaded %s " % records)
