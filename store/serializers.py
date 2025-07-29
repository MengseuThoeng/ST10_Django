from rest_framework import serializers

from store.models import Category, Products, Orders, Payment

# class CategorySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=200)
#     product_count = serializers.IntegerField(read_only=True)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'method', 'amount', 'is_paid', 'paid_at')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'qty', 'is_deleted', 'product', 'status')

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'description','product_count','status')

    def get_status(self, obj):
        count = getattr(obj, 'product_count', 0)
        if count == 0:
            return 'None'
        elif count <= 3:
            return 'Fewer'
        else:
            return 'Too many'

class ProductSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'qty', 'is_delete', 'created_date','categories','order_count')

# Serializer
# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     price = serializers.FloatField()
#     qty = serializers.IntegerField()
#     is_deleted = serializers.BooleanField(default=False)
#     created_date = serializers.DateTimeField()
#     categories = CategorySerializer(many=True, read_only=True)