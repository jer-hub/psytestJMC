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
            csv_reader = csv.reader(file, delimiter=",")
            choice_label = ""
            answer = None
            question_id = None
            for row in csv_reader:
                for sub_row in row[1:]:
                    if sub_row == "incorrect" or sub_row == "correct":
                        answer = sub_row
                        question_id = row[-1]
                        break
                    choice_label += sub_row
                        
                choice = Choice(
                    id=row[0],
                    choice=choice_label,
                    is_answer=answer,
                    question_id=question_id,

                )
                choice.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {choice.id}'))
