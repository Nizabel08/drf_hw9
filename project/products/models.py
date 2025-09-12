from django.db import models
from django.contrib.auth.models import User

class Product(models.Model) :
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    in_stock = models.BooleanField(default=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:  
        verbose_name = 'Product' 
        verbose_name_plural = 'Product' 

class ProductLog(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'log for {self.product.name} : {self.message[:30]}'

