from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Prepare the application for deployment'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting deployment preparation...')
        )
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', '--clear')
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate', '--noinput')
        
        self.stdout.write(
            self.style.SUCCESS('Deployment preparation completed successfully!')
        )
