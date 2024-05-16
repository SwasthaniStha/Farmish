from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_manage/', views.admin_manage, name='admin_manage'),
    path('admin_feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin_update_user/<int:user_id>/', views.admin_update_user, name='admin_update_user'),
    path('admin_delete_user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('feedback/<int:message_id>/', views.view_feedback, name='view_feedback'),
    path('feedback/reply/<int:message_id>/', views.reply_feedback, name='reply_feedback'),
    
    # Include the URLs of the 'product' app with the namespace 'product'
    path('product/', include('product.urls', namespace='product')),
    path('order_list/', views.order_list, name='order_list'),
]
