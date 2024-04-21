from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    if cart_products:
        return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})
    else:
        return render(request, "cart_summary.html")

@login_required
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Check if action is 'post'
    if request.POST.get('action') == 'post':
        # Get the product ID and quantity from the POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup the product in the database
        product = get_object_or_404(Product, id=product_id)

        # Check if the product exists
        if product:
            # Add the product to the cart
            cart.add(product=product, quantity=product_qty)

            # Get the updated cart quantity
            cart_quantity = len(cart)

            # Return response with cart quantity
            response = JsonResponse({'qty': cart_quantity})
            messages.success(request, "Product Added To Cart...")
            return response
        else:
            # Product not found, return error response
            return JsonResponse({'error': 'Product not found'}, status=404)

@login_required
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get the product ID from the POST data
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product_id)
        # Return success response
        response = JsonResponse({'success': 'Item Deleted From Shopping Cart...'})
        messages.success(request, "Item Deleted From Shopping Cart...")
        return response

@login_required
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get the product ID and quantity from the POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Update the quantity of the product in the cart
        cart.update(product_id, product_qty)
        # Return success response
        response = JsonResponse({'success': 'Your Cart Has Been Updated...'})
        messages.success(request, "Your Cart Has Been Updated...")
        return response
