import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Category, Products, Orders


class Command(BaseCommand):
    help = 'Generate fake data for Categories, Products, and Orders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create (default: 10)'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=100,
            help='Number of products to create (default: 100)'
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=200,
            help='Number of orders to create (default: 200)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    def handle(self, *args, **options):
        fake = Faker()

        # Clear existing data if requested
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Orders.objects.all().delete()
            Products.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Category names for more realistic data
        category_names = [
            'Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports',
            'Toys', 'Health & Beauty', 'Automotive', 'Food & Beverage', 'Music',
            'Movies', 'Games', 'Tools', 'Jewelry', 'Art & Crafts'
        ]

        # Create Categories
        categories = []
        categories_count = options['categories']

        for i in range(categories_count):
            category_name = category_names[i % len(category_names)]
            if i >= len(category_names):
                category_name += f" {i // len(category_names) + 1}"

            category = Category.objects.create(
                name=category_name,
                description=fake.paragraph(nb_sentences=random.randint(1, 3))
            )
            categories.append(category)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {categories_count} Categories.')
        )

        # Product name prefixes for different categories
        product_prefixes = {
            'Electronics': ['Smart', 'Digital', 'Wireless', 'Portable', 'HD'],
            'Books': ['Complete', 'Essential', 'Ultimate', 'Comprehensive', 'Advanced'],
            'Clothing': ['Premium', 'Classic', 'Trendy', 'Comfortable', 'Stylish'],
            'Home & Garden': ['Elegant', 'Practical', 'Modern', 'Decorative', 'Functional'],
            'Sports': ['Professional', 'Outdoor', 'Training', 'Competition', 'Fitness']
        }

        # Create Products
        products = []
        products_count = options['products']

        for _ in range(products_count):
            # Create product
            product = Products.objects.create(
                name=fake.catch_phrase().title(),
                price=round(random.uniform(5.99, 999.99), 2),
                qty=random.randint(0, 100),
                is_delete=random.choice([True, False]) if random.random() < 0.1 else False
            )

            # Assign 1-3 random categories to each product
            num_categories = random.randint(1, min(3, len(categories)))
            selected_categories = random.sample(categories, num_categories)
            product.categories.set(selected_categories)

            products.append(product)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {products_count} Products.')
        )

        # Create Orders
        orders_count = options['orders']
        status_choices = ['Pending', 'Completed', 'Cancelled']

        for _ in range(orders_count):
            # Only create orders for products that are not deleted
            available_products = [p for p in products if not p.is_delete]
            if not available_products:
                available_products = products  # Fallback if all products are deleted

            Orders.objects.create(
                qty=random.randint(1, 10),
                is_deleted=random.choice([True, False]) if random.random() < 0.15 else False,
                product=random.choice(available_products),
                status=random.choice(status_choices)
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {orders_count} Orders.')
        )

        # Print summary statistics
        self.stdout.write(self.style.SUCCESS('\n--- DATA SUMMARY ---'))
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Products: {Products.objects.count()}')
        self.stdout.write(f'Orders: {Orders.objects.count()}')

        # Show category distribution
        self.stdout.write('\n--- CATEGORY DISTRIBUTION ---')
        for category in Category.objects.all():
            product_count = category.products.count()
            self.stdout.write(f'{category.name}: {product_count} products')

        self.stdout.write(self.style.SUCCESS('\nFake data generation completed successfully!'))