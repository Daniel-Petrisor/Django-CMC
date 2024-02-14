# Import data from CSV to the database using the custom command.
# -----------------------------------------------------------------
from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv

# Proposed command = python manage.py importdata file_path model_name next_argument
# Proposed output = Data imported successfully!
# ! for more datasets gow to www.kaggle.com/datasets


class Command(BaseCommand):
    help = 'Import data from CSV file to the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file') # file_path
        parser.add_argument('model_name', type=str, help='Name of the model') # model_name
        # parser.add_argument('next_argument', type=str, help='Next argument') # next_argument


    def handle(self, *args, **kwargs):
        # logic data here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = None
        # Seearch for the model across all installed apps
        for app_config in apps.get_app_configs():
            # Try to search for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break # Stop searching if the model is found
            except LookupError:
                continue # Continue searching in the next app if the model is not found


        if not model:   # If the model is not found
            raise CommandError(f'Model "{model_name}" not found in any app!')

        print(f'File path: {file_path}')

        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Student.objects.create(**row)
                model.objects.create(**row)
                
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))