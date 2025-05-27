from django.contrib import admin

from store.models import Orders, Products, Category


# Register your models here.
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(Category)