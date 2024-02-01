from typing import Any
from django.core.management.base import BaseCommand



# Proposed command = python manage.py greeting Name
# Proposed output = Hi { Name }, Goog Morning!
class Command(BaseCommand):
    help = ' Greets the user'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        greeting = f'Hi {name}, Goog Morning!'
        # self.stdout.write(greeting)
        self.stdout.write(self.style.SUCCESS(greeting))
