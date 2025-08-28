from rest_framework import serializers

from store.models import Category, Products, Orders, Payment, UserProfile
from djoser.serializers import UserCreateSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# class CategorySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=200)
#     product_count = serializers.IntegerField(read_only=True)


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        phone_data = self.initial_data.pop('phone', None)
        address_data = self.initial_data.pop('address', None)
        city_data = self.initial_data.pop('city', None)
        state_data = self.initial_data.pop('state', None)
        zipcode_data = self.initial_data.pop('zipcode', None)
        print("Initial Data:", self.initial_data)

        user = super().create(validated_data)
        print("Phone Data:", phone_data)
        if phone_data:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': phone_data,
                    'address': address_data,
                    'city': city_data,
                    'state': state_data,
                    'zipcode': zipcode_data,
                }
            )
        return user


# class UserProfileSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name')


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
        fields = ('id', 'name', 'description', 'product_count', 'status')

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
        fields = ('id', 'name', 'price', 'qty', 'is_delete', 'created_date', 'categories', 'order_count')

# Serializer
# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     price = serializers.FloatField()
#     qty = serializers.IntegerField()
#     is_deleted = serializers.BooleanField(default=False)
#     created_date = serializers.DateTimeField()
#     categories = CategorySerializer(many=True, read_only=True)
