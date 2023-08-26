import environ
from diffy.users.models import User
from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Creates an admin account for faster setup."

    def handle(self, *args, **options):
        env = environ.Env()
        environ.Env.read_env()

        if env("ADMIN_EMAIL", default=None) and env("ADMIN_PASSWORD", default=None):
            if not User.objects.filter(email=env("ADMIN_EMAIL")).exists():
                sa = User(email=env("ADMIN_EMAIL"),
                          is_staff=True,
                          is_superuser=True)
                sa.save()
                sa.set_password(env("ADMIN_PASSWORD"))
                sa.save()
                token = Token(user=sa)
                if env("ADMIN_TOKEN", default=None):
                    token.key = env("ADMIN_TOKEN")
                token.save()
                print("Created admin super user and token.")
            else:
                print('Admin exists, skipping creation.')
        else:
            print('Admin environment variables not found.')