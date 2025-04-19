from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create or update a default superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'customer'
        email = 'customer@gmail.com'
        password = 'Customer@1234'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})

        if created:
            user.set_password(password)
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Customer created successfully.'))
        else:
            # Optional: reset password if needed
            if not user.check_password(password):
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.WARNING('Password was incorrect. It has been updated.'))
            else:
                self.stdout.write(self.style.WARNING('Customer already exists with correct password.'))
