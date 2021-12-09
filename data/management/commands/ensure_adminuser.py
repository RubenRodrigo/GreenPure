from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")
        parser.add_argument('--firstname', help="Admin's firstname")
        parser.add_argument('--lastname', help="Admin's lastname")

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email=options['email']).exists():
            User.objects.create_superuser(email=options['email'],
                                          password=options['password'],
                                          first_name=options['firstname'],
                                          last_name=options['lastname'])
            print("Usuario creado")
        else:
            print("Usuario ya existe")