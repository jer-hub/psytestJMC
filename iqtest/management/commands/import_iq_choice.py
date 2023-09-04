import csv
from django.core.management.base import BaseCommand
from iqtest.models import Choice

class Command(BaseCommand):
    help = 'Import data from a CSV file into the model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_data(csv_file)

    def import_data(self, csv_file):
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                choice = Choice(
                    id=row['id'],
                    choice=row['choice'],
                    is_answer=row['is_answer'],
                    question_id=row['question_id'],

                )
                choice.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {choice}'))
