from django.contrib import admin
from product.models import Product, Category, Customer, Messages_from_farmers

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Messages_from_farmers)


