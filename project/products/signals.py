from .models import Product, ProductLog
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender = Product)
def log_product_creation(sender, instance, created, **kwargs) :
    if created :
        ProductLog.objects.create(
            product = instance,
            message = f'product {instance.name} was created'
        )
    else :
        ProductLog.objects.create(
            product = instance,
            message = f'product {instance.name} was updated'
        )


# @receiver(post_delete, sender = Product) 
# def log_product_delete(sender, instance, **kwargs) :
#     ProductLog.objects.create(
#         product = None,
#         message = f'product "{instance.name}" was deleted'
#     )