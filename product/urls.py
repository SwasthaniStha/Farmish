from django.urls import path
from .views import add_product, product_list,view_product, about_us,contact_us,view_orders, login_user, logout_user, register_user, update_password, update_user,view_orders,update_order_status

app_name = 'product'

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('shop/', product_list, name='product_list'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
    path('product/<int:product_id>/', view_product, name='view_product'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('update_password/', update_password, name='update_password'),
    path('update_user/', update_user, name='update_user'),
    path('orders/', view_orders, name='orders'),
    path('orders/<int:order_id>/update/', update_order_status, name='update_order_status'),
]
