from django.contrib import admin
from .models import Product
# Register your models here.

admin.site.site_header = "Nizabel's shop"
admin.site.site_title = 'My shop portal🐥'
admin.site.index_title = 'Shop portal'


@admin.action(description='mark selected products as outof-stock')
def mark_out_of_stock(modeladmin, request, queryset) :
    queryset.update(in_stock = False)

@admin.action(description='mark selected products as in-stock')
def mark_in_stock(modeladmin, request, queryset) :
    queryset.update(in_stock = True)

@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin) :
    list_display = ('name', 'price', 'in_stock')
    list_filter = ('in_stock',) 
    search_fields = ('name',)   
    ordering = ('-price',)   
    actions = [mark_in_stock, mark_out_of_stock]





