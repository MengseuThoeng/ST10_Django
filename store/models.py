from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    city = models.CharField(max_length=255,blank=True)
    state = models.CharField(max_length=255,blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return f"{self.user.username} - {self.user.email} - {self.phone}"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return 'https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png'



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # products = models.ManyToManyField('Products', related_name='products', blank=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return f"{self.name}"


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    qty = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f"{self.name}"


class Orders(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    qty = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"{self.qty} - ${self.is_deleted} - {self.product.name}"


class Payment(models.Model):
    order = models.OneToOneField(Orders, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=50)  # e.g. 'Credit Card', 'Cash', 'ABA Pay'
    amount = models.FloatField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment for Order #{self.order.id} - ${self.amount} - {self.method}"

