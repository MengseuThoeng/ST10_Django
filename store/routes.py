from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet)

urlpatterns = router.urls


# urlpatterns = [
#     # path('products/' ,views.ProductList.as_view()),
#     # path('products/<id>/', views.ProductDetail.as_view()),
#     # path('categories/', views.CategoryList.as_view()),
#     # path('categories/<id>/', views.CategoryDetail.as_view()),
# ]
