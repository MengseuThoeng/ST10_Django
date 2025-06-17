from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Products
from .serializers import ProductSerializer


@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        all_products = Products.objects.all()
        obj = ProductSerializer(all_products, many=True)
        return Response(obj.data)
    elif request.method == 'POST':
        new_products = ProductSerializer(data=request.data)
        if new_products.is_valid():
            new_products.save()
            return Response(new_products.data, status=status.HTTP_201_CREATED)
        return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def show(request, id):
    product = get_object_or_404(Products, id=id)
    if request.method == 'GET':
        obj = ProductSerializer(product)
        return Response(obj.data)
    elif request.method == 'PUT':
        new_products = ProductSerializer(data=request.data)
        if new_products.is_valid():
            new_products.save()
            return Response(new_products.data)
        return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        new_products = ProductSerializer(product, data=request.data, partial=True)
        if new_products.is_valid():
            new_products.save()
            return Response(new_products.data)
        return Response(new_products.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
    # try:
    #     products = Products.objects.get(id=id)
    #     obj = ProductSerializer(products, many=False)
    # except Products.DoesNotExist:
    #     return Response({"error": "product not found"},status=404)
    # return Response(obj.data)

# Create your views here.
# def home(request):
#     print(request.GET.get('name'))
#     return render(request,'app.html')
#
# def product(request):
#     return render(request,'product.html')
