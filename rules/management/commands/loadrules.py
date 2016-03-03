import os
from django.core.management.base import BaseCommand
from django.conf import settings
from rules.models import load_rules


class Command(BaseCommand):
    help = "generate bank accounts for validation with approx 5% invalids"

    def handle(self, *args, **options):
        filename = input("Enter rules file to be loaded (hit enter for valacdos.txt in MEDIA_ROOT): ")
        if not filename:
            filename = os.path.join(settings.MEDIA_ROOT, 'valacdos.txt')
        try:
            records = load_rules(filename)
            self.stdout.write("Records Loaded %s " % records)
        except (IOError, RuntimeError):
            self.stdout.write('Cant open file: %s - or file is corrupt' % filename)
