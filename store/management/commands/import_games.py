import csv
from django.core.management.base import BaseCommand
from store.models import Game
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Import games from CSV file'

    def handle(self, *args, **options):
        csv_file = os.path.join(settings.BASE_DIR, 'data/items.csv')

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Game.objects.create(
                    title=row['title'],
                    description=row['description'],
                    price=row['price'],
                    location=row['location']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported games'))