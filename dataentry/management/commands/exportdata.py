# Export data from CSV using the custom command.
# -----------------------------------------------------------------
from django.core.management.base import BaseCommand
# from dataentry.models import Student # 1
from django.apps import apps
import datetime
import csv

# Proposed command = python manage.py exportdata
# Proposed command = python manage.py exportdata model_name

class Command(BaseCommand):
    # help = 'Export data from Student model to CSV file.' # 1
    help = 'Export data from database to CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model') # model_name

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # search through all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # Stop searching if the model is found
            except LookupError:
                pass # Continue searching in the next app if the model is not found

        
        if not model:   # If the model is not found
            self.stderr.write(f'Model "{model_name}" not found')
            return
        



        # fetch data from database
        # students = Student.objects.all() # 1
        data = model.objects.all()

        # generate the timestamp off current date and time
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        # define the csv file name/path
        # file_path = f'exported_students_data_{timestamp}.csv' # 1
        file_path = f'exported_{model_name}_data_{timestamp}.csv'

        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the CSV header
            # writer.writerow(['Roll No', 'Name', 'Age']) # 1
            # we want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields]) # Header


            # write the data rows
            # for student in students: # 1
            #     writer.writerow([student.roll_no, student.name, student.age]) # 1
            
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields]) # Header

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))