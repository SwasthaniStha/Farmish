from django.urls import path
from .views import add_product, product_list, about_us,view_product,contact_us,Order

urlpatterns = [
    path('', add_product, name='add_product'),
    path('shop/', product_list, name='product_list'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
    path('Order/', Order, name='Order'),
    path('product/<int:product_id>/', view_product, name='view_product'),
    
]
