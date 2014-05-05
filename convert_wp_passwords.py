from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import get_hasher


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ 
        Converts passwords with the default wordpress phpass algorithm
        to be readable by Django.
        """
        # command to run: python manage.py convert_wp_passwords

        User = get_user_model()
        hasher = get_hasher('phpass')

        users = User.objects.filter(password__startswith='$P$B')
        for user in users:
            user.password = hasher.from_orig(user.password)
            user.save()
            print user.pk

        print "%s User passwords converted" % len(users)
