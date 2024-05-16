from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile
from product.models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ContactForm, ReplyForm

from store.models import Messages_from_users
from product.models import Messages_from_farmers

from product.models import Product
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from payment.models import OrderItem, Order

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from django.core.exceptions import ObjectDoesNotExist

def is_admin(user):
    return user.is_authenticated and user.profile.is_admin

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.all().count()
    total_farmers = Profile.objects.filter(is_farmer=True).count()
    total_customers = Profile.objects.filter(is_customer=True).count()
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'admin_dashboard.html', {'total_users': total_users, 'total_farmers': total_farmers, 'total_customers': total_customers, 'recent_users' : recent_users})

@user_passes_test(is_admin)
def admin_manage(request):
    users = User.objects.all()
    return render(request, 'admin_manage.html', {'users': users, 'user_type': 'admin'})

def admin_update_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        is_farmer = request.POST.get('is_farmer')
        is_customer = request.POST.get('is_customer')
        user.profile.is_farmer = is_farmer == 'on'
        user.profile.is_customer = is_customer == 'on'    
        user.profile.save()
        messages.success(request, f'{user.username} updated successfully!')
        return redirect('admin_manage')
    context = {'user': user}
    return render(request, 'admin_update_user.html', context)

def admin_delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    messages.success(request, f'{user.username} deleted successfully!')
    return HttpResponseRedirect(reverse('admin_manage'))

def admin_feedback(request):
    messages_from_users = Messages_from_users.objects.all()
    messages_from_farmers = Messages_from_farmers.objects.all()

    return render(request, 'admin_feedback.html', {'messages_from_users': messages_from_users, 'messages_from_farmers': messages_from_farmers})

def view_feedback(request, message_id):
    message = get_object_or_404(Messages_from_users, id=message_id)
    form = ReplyForm()
    return render(request, 'view_feedback.html', {'message': message, 'form': form})


def reply_feedback(request, message_id):
    message = get_object_or_404(Messages_from_users, id=message_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_message = form.cleaned_data['reply_message']
            subject = "Reply to Your Feedback"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [message.email]
            try:
                send_mail(subject, reply_message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Your reply has been sent.')
                return redirect('admin_feedback')
            except Exception as e:
                messages.error(request, f'Failed to send the reply. Error: {e}')
        else:
            messages.error(request, 'Invalid form submission. Email not sent.')
    else:
        form = ReplyForm()
    return render(request, 'view_feedback.html', {'message': message, 'form': form})

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(product_name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	


def update_info(request):
	if not request.user.is_authenticated:
		messages.error(request, "You must be logged in to access that page!!")
		return redirect('home')
	
	try:
		# Get Current User
		current_user = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		messages.error(request, "Profile not found.")
		return redirect('home')
		# Get Current User's Shipping Info
	shipping_user, created = ShippingAddress.objects.get_or_create(user_id=request.user.id)
		
		# Get original User Form
	if request.method == 'POST':
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		

		if form.is_valid() and shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
	else:
		form = UserInfoForm(instance = current_user)
		shipping_form = ShippingForm(instance = shipping_user)

	return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
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
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    print(categories) 
    return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    
    try:
        # Look Up The Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except ObjectDoesNotExist:
        messages.error(request, "Category Does Not Exist")
        return redirect('home')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})	

def contact_us(request):
	return render(request, 'contact_us.html', {})	

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user_profile = Profile.objects.get(user=user)

            # Check if the user is a farmer or consumer
            if current_user_profile.is_farmer:
                return redirect('product:product_list')
            else:
                # Get their saved cart from the database
                saved_cart = current_user_profile.old_cart
                # Convert database string to python dictionary
                if saved_cart:
                    # Convert to dictionary using JSON
                    converted_cart = json.loads(saved_cart)
                    # Add the loaded cart dictionary to our session
                    # Get the cart
                    cart = Cart(request)
                    # Loop thru the cart and add the items from the database
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)

                messages.success(request, "You Have Been Logged In!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
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

from django.contrib.auth.decorators import login_required
from payment.models import Order

@login_required
def order_list(request):
    order_items = OrderItem.objects.filter(user=request.user).select_related('order', 'product')
    context = {'order_items': order_items}
    return render(request, 'order_list.html', context)