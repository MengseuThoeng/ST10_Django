from rest_framework import serializers

from store.models import Category, Products, Orders, Payment, UserProfile, Post
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


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 
                  'address', 'phone', 'city', 'state', 'zipcode', 'avatar')


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


class PostSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_by', 'created_by_username', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('created_by', 'created_at', 'updated_at')


# Serializer
# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     price = serializers.FloatField()
#     qty = serializers.IntegerField()
#     is_deleted = serializers.BooleanField(default=False)
#     created_date = serializers.DateTimeField()
#     categories = CategorySerializer(many=True, read_only=True)
