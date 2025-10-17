from django.db.models import Count
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from djoser.utils import decode_uid

from .models import Products, Category, Orders, Payment, UserProfile, Post
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, PaymentSerializer, UserProfileSerializer, PostSerializer

User = get_user_model()


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users: Can do everything (GET, POST, PUT, DELETE)
    - Regular users: Can only read (GET)
    - Unauthenticated users: No access
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return False


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()  # <--- add this!
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrReadOnly]  

    def get_queryset(self):
        return Payment.objects.filter(order_id=self.kwargs['order_pk'])

    def perform_create(self, serializer):
        serializer.save(order_id=self.kwargs['order_pk'])


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]  

    def get_queryset(self):
        # 1. For nested router: /categories/<category_pk>/products/
        category_pk = self.kwargs.get('category_pk')
        # 2. For query param: /products?category=1
        category_id = self.request.query_params.get('category', None)

        qs = Products.objects.annotate(order_count=Count('orders'))

        # Priority: nested router > query param
        if category_pk is not None:
            qs = qs.filter(categories=category_pk)
        elif category_id is not None:
            qs = qs.filter(categories=category_id)
        return qs




class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        product_count=Count('products')
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  


class OrderViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]  


@api_view(['GET', 'POST'])
def activate_user(request, uid, token):
    """
    Activate user account from email link
    """
    try:
        from django.contrib.auth.tokens import default_token_generator
        
        # Decode the uid to get user_id
        user_id = decode_uid(uid)
        user = User.objects.get(pk=user_id)
        
        # Check if token is valid using Django's default token generator
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({
                "detail": "Account activated successfully! You can now login.",
                "user_id": user.id,
                "email": user.email,
                "is_active": user.is_active
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Invalid or expired activation token."
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except (User.DoesNotExist, ValueError, TypeError) as e:
        return Response({
            "detail": f"Invalid activation link. Error: {str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get current user info based on JWT token
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        # If user doesn't have a profile yet, create one
        user_profile = UserProfile.objects.create(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(ModelViewSet):
    """
    ViewSet for Post model where users can only see and manage their own posts.
    Admins can see all posts.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter posts: 
        - Admins can see all posts
        - Regular users can only see their own posts
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the created_by field to the current user
        """
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Only allow users to retrieve their own posts (or admins to retrieve any)
        """
        instance = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            if instance.created_by != request.user:
                return Response(
                    {"detail": "You do not have permission to view this post."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Only allow users to update their own posts
        """
        instance = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            if instance.created_by != request.user:
                return Response(
                    {"detail": "You do not have permission to edit this post."},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Only allow users to delete their own posts
        """
        instance = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            if instance.created_by != request.user:
                return Response(
                    {"detail": "You do not have permission to delete this post."},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().destroy(request, *args, **kwargs)



# Second Short
# class ProductList(ListCreateAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     # def get_queryset(self):
#     #     return Products.objects.all()
#     #
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'
#
# class CategoryList(ListCreateAPIView):
#     queryset = Category.objects.annotate(
#         product_count = Count('products')
#     )
#     serializer_class =  CategorySerializer
#
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'id'

# api view
# @api_view(['GET', 'POST'])
# def index(request):
#     if request.method == 'GET':
#         all_products = Products.objects.all()
#         obj = ProductSerializer(all_products, many=True)
#         return Response(obj.data)
#     elif request.method == 'POST':
#         new_products = ProductSerializer(data=request.data)
#         if new_products.is_valid():
#             new_products.save()
#             return Response(new_products.data, status=status.HTTP_201_CREATED)
#         return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
#     return None
#
#
# @api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
# def show(request, id):
#     product = get_object_or_404(Products, id=id)
#     if request.method == 'GET':
#         obj = ProductSerializer(product)
#         return Response(obj.data)
#     elif request.method == 'PUT':
#         new_products = ProductSerializer(data=request.data)
#         if new_products.is_valid():
#             new_products.save()
#             return Response(new_products.data)
#         return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PATCH':
#         new_products = ProductSerializer(product, data=request.data, partial=True)
#         if new_products.is_valid():
#             new_products.save()
#             return Response(new_products.data)
#         return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
#     return None
#     # try:
#     #     products = Products.objects.get(id=id)
#     #     obj = ProductSerializer(products, many=False)
#     # except Products.DoesNotExist:
#     #     return Response({"error": "product not found"},status=404)
#     # return Response(obj.data)

# Create your views here.
# def home(request):
#     print(request.GET.get('name'))
#     return render(request,'app.html')
#
# def product(request):
#     return render(request,'product.html')
