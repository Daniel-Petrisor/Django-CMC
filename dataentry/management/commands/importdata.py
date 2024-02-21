# Import data from CSV to the database using the custom command.
# -----------------------------------------------------------------
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError
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
        
        # compare csv header with model's fields names
        # get all the fields names of the model that we found
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path) as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f'CSV header "{csv_header}" does not match model fields "{model_fields}"!')


            for row in reader:
                # Student.objects.create(**row)
                model.objects.create(**row)
                
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))