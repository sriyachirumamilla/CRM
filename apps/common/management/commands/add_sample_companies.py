from django.core.management.base import BaseCommand
from apps.common.models import Company

class Command(BaseCommand):
    help = 'Add sample companies to the database'

    def handle(self, *args, **kwargs):
        Company.objects.create(
            name="Tech Innovations Inc.",
            address="100 Tech Lane",
            contact_number="123-456-7890"
        )
        Company.objects.create(
            name="Green Solutions Ltd.",
            address="200 Green Road",
            contact_number="234-567-8901"
        )
        Company.objects.create(
            name="Global Enterprises",
            address="300 Global Avenue",
            contact_number="345-678-9012"
        )
        self.stdout.write(self.style.SUCCESS('Successfully added sample companies'))
