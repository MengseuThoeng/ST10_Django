import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Category, Products, Orders


class Command(BaseCommand):
    help = 'Generate fake data for Categories, Products, and Orders'

    def handle(self, *args, **options):
        fake = Faker()

        # Create Categories
        categories = []
        for _ in range(10):
            category = Category.objects.create(
                name=fake.word().capitalize(),
                description=fake.sentence()
            )
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 Categories.'))

        # Create Products
        products = []
        for _ in range(100):
            product = Products.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),
                price=round(random.uniform(1.0, 100.0), 2),
                qty=random.randint(1, 50),
                category=random.choice(categories)
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f'Successfully created 100 Products.'))

        # Create Orders
        for _ in range(200):
            Orders.objects.create(
                qty=random.randint(1, 10),
                is_deleted=random.choice([True, False]),
                product=random.choice(products)
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created 200 Orders.'))
