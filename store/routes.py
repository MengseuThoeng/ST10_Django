from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet)
# router.register('reviews', views.ReviewViewSet)

payment_router = NestedDefaultRouter(router, 'orders', lookup='order')
payment_router.register('payments', views.PaymentViewSet)

category_products_router = NestedDefaultRouter(router, 'categories', lookup='category')
category_products_router.register('products', views.ProductViewSet, basename='category-products')

urlpatterns = router.urls + payment_router.urls + category_products_router.urls



# urlpatterns = [
#     # path('products/' ,views.ProductList.as_view()),
#     # path('products/<id>/', views.ProductDetail.as_view()),
#     # path('categories/', views.CategoryList.as_view()),
#     # path('categories/<id>/', views.CategoryDetail.as_view()),
# ]
