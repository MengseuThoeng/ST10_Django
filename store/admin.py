from django.contrib import admin

from store.models import Orders, Products, Category


# Register your models here.
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'total', 'status', 'is_deleted')
    list_editable = ('status', 'is_deleted')
    list_per_page = 10
    search_fields = ('product__name',)

    def total(self, order: Orders):
        return int(order.qty * order.product.price)

    total.short_description = 'Total'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')

    def desc(self, category: Category):
        words = category.description.split(' ')
        return " ".join(words[:3]) + "..."

    desc.short_description = 'Desc'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_delete']
    list_editable = ['is_delete']
    list_per_page = 10
    search_fields = ('name',)
