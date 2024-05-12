from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.payment, name='payment'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name = "billing_info"),
]
