from django.urls import path
from .views import *

urlpatterns = [
    path("create/", CreateProductAPIView.as_view(), name="create-product"),
    path("list-products/", ListProductViewSet.as_view(), name="list-products"),
    path('edit-stock/<uuid:id>', EditStockView.as_view(), name='edit-stock'),
]
