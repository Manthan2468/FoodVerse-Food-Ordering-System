from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from decimal import Decimal

# Create your views here.

def add_to_cart(request):
    context = {
        'page': 'Add to Cart',
    }
    return redirect('cart')

def cart_page(request):

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    subtotal = 0

    for item in cart_items:
        subtotal += item.product.price * item.quantity
    delivery_charges = 50
    if subtotal > 200 or subtotal == 0:
        delivery_charges = 0

    tax = subtotal * Decimal('0.05')
    grand_total = subtotal + delivery_charges + tax

    context = {
        'page': 'Cart',
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charges': delivery_charges,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request,'cart.html',context)

def increase_quantity(request, id):
    if request.user.is_authenticated:
        cart_items = get_object_or_404(CartItem, id = id, cart__user=request.user)

        cart_items.quantity += 1
        cart_items.save()

    return redirect('cart_page')

def decrease_quantity(request, id):
    if request.user.is_authenticated:
        cart_items = get_object_or_404(CartItem, id = id, cart__user=request.user)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()

    return redirect('cart_page')

def remove_item(request, id):
    if request.user.is_authenticated:
        cart_items = get_object_or_404(CartItem, id = id, cart__user=request.user)

        cart_items.delete()

    return redirect('cart_page')

def update_cart_quantity(request):
    context = {
        'page': 'Update Cart',
    }
    return redirect('cart')

def remove_cart_item(request):
    context = {
        'page': 'Remove Cart',
    }
    return redirect('cart')

def checkout(request):
    context = {
        'page': 'Checkout',
    }
    return render(request,'checkout.html',context)

def place_order(request):
    context = {
        'page': 'Place Order',
    }
    return redirect('order_success')

def order_success(request):
    context = {
        'page': 'Success Order',
    }
    return render(request,'order_success.html',context)

def my_orders(request):
    context = {
        'page': 'My Orders',
    }
    return render(request,'my_orders.html',context)

def order_tracking(request):
    context = {
        'page': 'Tracking Order',
    }
    return render(request,'order_tracking.html',context)

def address_book(request):
    context = {
        'page': 'Address Book',
    }
    return render(request,'address_book.html',context)