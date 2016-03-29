from django.contrib.auth.models import User
from os import path
from django.conf import settings
from rest_framework.authtoken.models import Token

from rules.models import load_rules


def load_test_rules():
    load_test_user()
    sort_codes = ['070116', '074456', '086086', '086090', '089999',  '09999', '0X9999', '107999',
                  '118765', '123123', '134020', '180002', '200915', '202959', '203099', '300008',
                  '309070', '500000', '772798', '820000', '827101', '827999',' 871427', '872427',
                  '938063', '938600', '938611', '309634', '400000' ]
    load_rules(path.join(settings.MEDIA_ROOT, 'valacdos.txt'), sort_codes)


def load_test_user():
    user=User.objects.create_superuser('graham', 'chesters99@yahoo.com', 'testpass')
    Token.objects.get_or_create(user=user)
