import csv
from django.core.management.base import BaseCommand
from iqtest.models import Question
from django_quill.quill import Quill

class Command(BaseCommand):
    help = 'Import data from a CSV file into the model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_data(csv_file)

    def import_data(self, csv_file):
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',',escapechar="'")
            count = 0
            for row in csv_reader:
                count+=1
                # if count == 16 or count == 21 or count == 27:
                #     continue
                if count == 30 or count == 31:
                    # print(row["extra"])
                    row["question"] += row["extra"]
                question = Question(
                    id=row["id"],
                    question=row["question"])
                
                question.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {question.id}'))
