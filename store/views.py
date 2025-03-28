from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    print(request.GET.get('name'))
    return render(request,'app.html')

def product(request):
    return render(request,'product.html')
