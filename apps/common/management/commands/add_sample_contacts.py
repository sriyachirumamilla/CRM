from django.core.management.base import BaseCommand
from apps.common.models import Contact

class Command(BaseCommand):
    help = 'Add sample contacts to the database'

    def handle(self, *args, **kwargs):
        Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Elm Street"
        )
        Contact.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone_number="987-654-3210",
            address="456 Oak Avenue"
        )
        Contact.objects.create(
            name="Alice Johnson",
            email="alice.johnson@example.com",
            phone_number="555-555-5555",
            address="789 Pine Road"
        )
        self.stdout.write(self.style.SUCCESS('Successfully added sample contacts'))
