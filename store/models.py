from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return f"{self.name} - {self.description}"


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'product'

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Orders(models.Model):
    qty = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"{self.qty} - ${self.is_deleted} - {self.product.name}"