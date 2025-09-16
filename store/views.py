from django.db.models import Count
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Products, Category, Orders, Payment
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, PaymentSerializer


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
