from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ContactForm
from product.models import Category, Product
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart
from django.core.exceptions import ObjectDoesNotExist

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(product_name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "That Product Does Not Exist...Please try Again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

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
            return render(request, "update_password.html", {'form': form})
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
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except ObjectDoesNotExist:
        messages.error(request, "Category Does Not Exist")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # This line saves the form data to the database
            form.save()

            # Add a success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')

            # Redirect to the same page (the form will be cleared)
            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Get the user type from the form
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.is_farmer and user_type == 'farmer':  # Check if user is farmer
                return redirect('product:product_list')  # Redirect to farmer dashboard
            elif not profile.is_farmer and user_type == 'consumer':  # Check if user is consumer
                return redirect('home')  # Redirect to consumer dashboard
            else:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
      
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...Thanks for stopping by...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
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
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return render(request, "register.html", {'form': form})
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
            return render(request, "register.html", {'form': form})
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form': form})