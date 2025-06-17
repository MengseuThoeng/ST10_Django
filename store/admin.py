from django.contrib import admin

from store.models import Orders, Products, Category


# Register your models here.
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'total', 'status', 'is_deleted')
    list_editable = ('status', 'is_deleted')
    list_per_page = 10
    search_fields = ('product__name',)
    list_filter = ('status', 'is_deleted')

    def total(self, order: Orders):
        return f"${order.qty * order.product.price:.2f}"

    total.short_description = 'Total'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'products_count')
    search_fields = ('name', 'description')

    def products_count(self, category: Category):
        return category.products.count()

    def desc(self, category: Category):
        if not category.description:
            return "No description"
        words = category.description.split(' ')
        if len(words) <= 3:
            return category.description
        return " ".join(words[:3]) + "..."

    desc.short_description = 'Description'
    products_count.short_description = 'Products Count'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'qty', 'get_categories', 'created_date', 'is_delete']
    list_editable = ['is_delete']
    list_per_page = 10
    search_fields = ('name',)
    list_filter = ('is_delete', 'created_date', 'categories')
    filter_horizontal = ('categories',)  # Makes M2M selection easier

    def get_categories(self, product: Products):
        """Display categories for the product in list view"""
        categories = product.categories.all()
        if categories.exists():
            return ", ".join([cat.name for cat in categories])
        return "No categories"

    get_categories.short_description = 'Categories'

