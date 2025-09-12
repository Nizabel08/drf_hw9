from django.urls import path
from . import  views

urlpatterns = [
    path('products/', views.product_list, name = 'product_list'),
    path('products/<int:pk>', views.product_detail, name = 'product_detail'),
    path('add/', views.add_product, name = 'add_product'),
    path('products/<int:pk>/admin_update', views.admin_update_product, name = 'admin_update_product'),
]
