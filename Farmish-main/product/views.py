from django.shortcuts import render,  get_object_or_404
from .forms import ProductForm
from store.models import Product, Order
from django.contrib import messages 

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
    else:
        form = ProductForm()
    
    return render(request, 'product/home.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/shop.html', {'products': products})


def about_us(request):
    return render(request, 'product/about_us.html')

def contact_us(request):
    return render(request, 'product/contact_us.html')

def order_view(request):
    orders = Order.objects.all()
    return render(request, 'product/order.html', {'orders': orders})

def view_product(request, product_id):
    # Retrieve the product object from the database
    product = get_object_or_404(Product, pk=product_id)

    # Render the product details template with the product object
    return render(request, 'product/product_detail.html', {'product': product})




