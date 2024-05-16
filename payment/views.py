from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product
from django.dispatch import Signal
from payment.models import OrderItem
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

def process_order(request):
	if request.POST:
		#Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()	

		payment_form = PaymentForm(request.POST or None)
		#Get Shipping Data
		my_shipping = request.session.get('my_shipping')
		

		#Gather order info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		#Create shipping address from session info 
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
		amount_paid = totals
		
		#Create an order
		if request.user.is_authenticated:
			user = request.user
			#create order
			create_order = Order(user = user, full_name = full_name, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
			create_order.save()

			#Add order items
			#get order id
			order_id = create_order.pk
			#get product info 
			for product in cart_products():
				#get product id
				product_id = product.id
				#get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.rate
				#get quantity
				for key, value in quantities().items():
					if int(key) == product.id:
						#create order item
						create_order_item = OrderItem(order_id = order_id, product_id =product_id, user =user, quantity= value, price= price)
						create_order_item.save()

			messages.success(request, "Order Placed!")
			return redirect('home')

		else:
			#not logged in
			#create order
			create_order = Order(full_name = full_name, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
			create_order.save() 

			messages.success(request, "Order Placed!")
			return redirect('home')
			

	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def billing_info(request):
	if request.POST:
		#Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		#Create a session with Shipping Info 
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping


		#Check to see if user is logged in
		if request.user.is_authenticated:
			#Get the billing form
			billing_form = PaymentForm
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
		else:
			#Not logged in
			billing_form = PaymentForm
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})


		shipping_form = request.POST
		return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

def payment(request):
	return render(request,"payment/payment.html", {})	


@login_required
def payment_success(request):
    # Retrieve the order items for the current user
    order_items = OrderItem.objects.filter(order__user=request.user)

    # Iterate over the order items and send email notifications
    for order_item in order_items:
        product = order_item.product
        quantity = order_item.quantity

        # Check if the product belongs to a farmer
        if product.farmer:
            # Send an email notification to the farmer
            subject = f"Your product {product.product_name} has been ordered"
            message = f"Dear {product.farmer.username},\n\n" \
                      f"Your product '{product.product_name}' has been ordered for a quantity of {quantity}.\n\n" \
                      f"Best regards,\nFarmish Team"
            recipient_list = [product.farmer.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)

    return render(request, "payment/payment_success.html", {})





