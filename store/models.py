from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    class Meta:
        db_table = 'product'


class Order(models.Model):
    qty = models.IntegerField()
    is_deleted = models.BooleanField(default=False)