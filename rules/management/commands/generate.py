import random
from django.core.management.base import BaseCommand
from accounts.utils.BankValidator import Validator
from rules.models import Rule


class Command(BaseCommand):
    help = "Rules file loader"

    def handle(self, *args, **options):
        count = int(input("How many accounts are to be generated: "))
        bv=Validator()
        valid = invalid =added = 0
        while count > valid + added:
            while True:
                sort_code = str(random.randint(100000,999999))
                r=Rule.objects.filter(start_sort__lte=sort_code, end_sort__gte=sort_code)
                if r or '500000' < sort_code < '503000':
                    break
            account_number = str(random.randint(10000000,99999999))
            result = bv.validate(sort_code, account_number)
            if result:
                print('%s-%s %s' %(sort_code, account_number, result))
                valid += 1
            else:
                if '500000' < sort_code < '503000':
                    added += 1
                    print('%s-%s %s' %(sort_code, account_number, result))
                invalid += 1
        print('Valid %s, Invalid %s, Added %s, Percent Valid %s, Percent Added %s'
              % (valid, invalid, added, 100 * valid/(invalid + valid), 100 * added/valid))
