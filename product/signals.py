from django.dispatch import receiver
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from payment.views import payment_success_signal
from .models import Notification

@receiver(payment_success_signal)
def handle_payment_success(sender, product_id, quantity, **kwargs):
    try:
        # Dynamically get the Product model
        Product = apps.get_model('product', 'Product')
        product = Product.objects.get(pk=product_id)
        
        # Check if the product belongs to the farmer
        if product.farmer == sender:
            # Create a notification for the farmer
            notification = Notification(
                user=product.farmer,
                message=f"New order for {product.product_name}, quantity: {quantity}"
            )
            notification.save()
    except ObjectDoesNotExist:
        pass