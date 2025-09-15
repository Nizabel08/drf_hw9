from django.urls import path
from . import  views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name = 'product_list'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('add/', views.AddProductView.as_view(), name = 'add_product'),
    path('products/<int:pk>/admin_update', views.AdminUpdateProductView.as_view(), name = 'admin_update_product'),
]
