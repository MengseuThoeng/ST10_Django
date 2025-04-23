import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Products


class Command(BaseCommand):
    help = 'Generate fake data'

    def handle(self, *args, **options):
        fake = Faker()
        number_of_product = 100
        for _ in range(number_of_product):
            Products.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),  # Random 2-word name
                price=round(random.uniform(1.0, 100.0), 2),  # Random price from $1 to $100
                qty=random.randint(1, 50),  # Random quantity from 1 to 50
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number_of_product} Product.'))
