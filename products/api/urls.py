from django.urls import path, include
from rest_framework.generics import DestroyAPIView
from rest_framework.routers import DefaultRouter
from products.api.views.general_views import MeasureUnitListAPIView, CategoryProductListAPIView, IndicatorListAPIView
from products.api.views.product_view import (
    ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView,
    ProductDestroyAPIView, ProductUpdateAPIView, ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView, ProductViewSet
)
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register(r'producto', ProductViewSet, basename='productos')

urlpatterns = [
    path('measure/', MeasureUnitListAPIView.as_view(), name='mesasure_list'),
    path('indicator/', IndicatorListAPIView.as_view(), name='indicator'),
    path('category/', CategoryProductListAPIView.as_view(), name='category'),
    path('product/list', ProductListAPIView.as_view(), name='product_list'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/retrieve/<int:pk>', ProductRetrieveAPIView.as_view(), name='product_retrieve'),
    path('product/destroy/<int:pk>', ProductDestroyAPIView.as_view(), name='product_destroy'),
    path('product/update/<int:pk>', ProductUpdateAPIView.as_view(), name='product_update'),
    path('product/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('product/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_retrieve_update_destroy'),
    path('', include((router.urls, 'api'))),
    path('docs/', include_docs_urls(title='API')),
]
