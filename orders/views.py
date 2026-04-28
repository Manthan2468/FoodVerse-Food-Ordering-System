from multiprocessing import context

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.

def user_check(request):
    if not request.user.is_authenticated:
        return redirect('login')

def cart_summery(request):
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
    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charges': delivery_charges,
        'tax': tax,
        'grand_total': grand_total,
    }


def add_to_cart(request):
    context = {
        'page': 'Add to Cart',
    }
    return redirect('cart')


def cart_page(request):
    user_check(request)
    context = cart_summery(request)
    context['page'] = 'Cart'
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
    user_check(request)
    context = cart_summery(request)
    address = DeliveryAddress.objects.filter(user=request.user, is_default=True).first()
    context['page'] = 'Checkout'
    context['address'] = address
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

def change_address(request):
    user_check(request)
    address = DeliveryAddress.objects.filter(user=request.user).order_by('-is_default')
    print(address)
    context = {
        'page': 'Change Address',
        'addresses': address,
    }
    return render(request,'change_address.html',context)

def add_new_address(request):
    user_check(request)
    if request.method == 'POST':

        DeliveryAddress.objects.create(
            user=request.user,
            full_name = request.POST['full_name'],
            phone = request.POST['phone'],
            address = request.POST['address'],
            city = request.POST['city'],
            state = request.POST['state'],
            pincode = request.POST['pincode'],
            is_default = False,
        )
        return redirect('/change_address/')
    context = {
        'page': 'Add New Address',
    }
    return render(request, 'add_new_address.html', context=context)


def make_default_address(request, id):
    DeliveryAddress.objects.filter(user=request.user).update(is_default=False)
    address = get_object_or_404(DeliveryAddress, id=id, user=request.user)
    address.is_default = True
    address.save()
    return redirect('change_address')


def update_address(request, id):
    address = get_object_or_404(DeliveryAddress, id=id, user=request.user)

    if request.method == 'POST':
        address.full_name = request.POST['full_name']
        address.phone = request.POST['phone']
        address.address = request.POST['address']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.pincode = request.POST['pincode']

        address.save()
        return redirect('change_address')

    context = {
        'page': 'Update Address',
        'address': address,
    }
    return render(request,'update_address.html',context)