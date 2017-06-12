from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = os.environ.get('ADMIN_USERNAME')
            password = os.environ.get('ADMIN_PASSWORD')
            email = os.environ.get('ADMIN_EMAIL')

            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(
                email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print(
                'Admin user can only be initialized if no Users exist')
