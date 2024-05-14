from django.shortcuts import render, redirect
from .forms import ProductForm, ChangePasswordForm, UpdateUserForm, SignUpForm, ContactFormFarmers
from store.models import Product, Order, Profile
from django.shortcuts import render, get_object_or_404
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from product.models import Notification
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from payment.models import Order, OrderItem

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
    if request.method == 'POST':
        form = ContactFormFarmers(request.POST)
        if form.is_valid():
            # This line saves the form data to the database
            form.save()

            # Add a success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')

            # Redirect to the same page (the form will be cleared)
            return redirect('product:contact_us')
    else:
        form = ContactFormFarmers()

    return render(request, 'product/contact_us.html', {'form': form})



def view_product(request, product_id):
    # Retrieve the product object from the database
    product = get_object_or_404(Product, pk=product_id)

    # Render the product details template with the product object
    return render(request, 'product/product_detail.html', {'product': product})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'product/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...Thanks for stopping by...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Activates the user immediately upon registration
            user.save()
            login(request, user)
            messages.success(request, "Your account has been created and is active.")

            # Send a welcome email to the new user
            subject = "Welcome to Farmish!"
            message = "Hello "+user.first_name+"!! \n"+"Welcome to Farmish. \n Thank you for visiting our website. We are glad to have you with us. \n. \n \n Thanking you, \n Farmish"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('home')
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
            return render(request, "register.html", {'form': form})
    else:
        form = SignUpForm()
        return render(request, "product/register.html", {'form': form})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, "Your Password Has Been Updated...")
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "product/update_password.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "product/update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

@login_required
def view_orders(request):
    orders = Order.objects.filter(product__farmer=request.user)
    order_items = OrderItem.objects.filter(order__in=orders)
    context = {
        'orders': orders,
        'order_items': order_items,
    }
    return render(request, 'product/order.html', context)

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, product__farmer=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
    context = {
        'order': order,
    }
    return render(request, 'product/update_order_status.html', context)