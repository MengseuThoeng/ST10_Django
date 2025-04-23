from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    qty = models.IntegerField()
    class Meta:
        db_table = 'product'


class Orders(models.Model):
    qty = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta:
        db_table = 'order'