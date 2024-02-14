
# I want to add some data to the database using the custom command.
# -----------------------------------------------------------------
from django.core.management.base import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help = 'It will insert data in the database.'

    def handle(self, *args, **kwargs):
        # logic data here

        # add 1 data
        # Student.objects.create(
        #     name='John',
        #     roll_no=1234567890,
        #     age=34,
        # )

        # add more data
        dataset = [
            {'name': 'Ross','roll_no': 235345,'age': 34},
            {'name': 'Jane','roll_no': 990773,'age': 33},
            {'name': 'Mike','roll_no': 435782,'age': 27},
            {'name': 'Jose','roll_no': 568793,'age': 56}, # new
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING('Student with roll no {roll_no} already exists!'))



        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))