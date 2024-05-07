from django.urls import path
from .views import add_product, product_list, about_us,view_product,contact_us,order_view, login_user, logout_user, register_user, update_password, update_user

app_name = 'product'

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('shop/', product_list, name='product_list'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
    path('Order/', order_view, name='Order'),
    path('product/<int:product_id>/', view_product, name='view_product'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('update_password/', update_password, name='update_password'),
    path('update_user/', update_user, name='update_user'),
]
