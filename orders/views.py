import json
from multiprocessing import context
from django.contrib.gis.db.backends.spatialite import client
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Food_Order import settings
from .models import *
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import razorpay

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

def checkout(request):
    user_check(request)
    context = cart_summery(request)
    address = DeliveryAddress.objects.filter(user=request.user, is_default=True).first()
    context['page'] = 'Checkout'
    context['address'] = address
    return render(request,'checkout.html',context)

def place_order(request):
    user = request.user
    user_check(request)

    if request.method == 'POST':
        payment_method = request.POST.get('payment')
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return redirect('cart_page')

        address = DeliveryAddress.objects.filter(user=user, is_default=True).first()

        cart_data = cart_summery(request)

        order = Order.objects.create(
            user = user,
            restaurant = cart_items.first().product.restaurant,
            address = address,
            total_amount = int(cart_data['grand_total']),
            delivery_fee = int(cart_data['delivery_charges']),
            payment_method = 'COD' if payment_method == 'COD' else 'Online'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price,
            )

        if payment_method == "COD":
            cart_items.delete()
            return redirect('order_success', id=order.id)

        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = client.order.create({
            "amount" : int(float(cart_data['grand_total']) * 100),
            "currency" : "INR",
            "payment_capture" : 1
        })

        request.session['razorpay_order_id'] = payment['id']
        request.session['order_id'] = order.id

        context = {
            'page': 'Place Order',
            'payment': payment,
            'razorpay_key' : settings.RAZORPAY_KEY_ID,
            'amount' : cart_data['grand_total'],
            'address' : address,
            'order_id' : order.id
        }

        return render(request, 'razorpay_payment.html', context)

    return redirect('order_success')


def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # DEBUG: print what you received
        print("Received data:", data)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            order_id = request.session.get('order_id')
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart).delete()

            return JsonResponse({'status': 'success', 'order_id': order_id})

        except Exception as e:
            print("Verification error:", e)  # <-- see actual error
            return JsonResponse({'status': 'failed', 'error': str(e)})

def order_success(request, id):
    order = Order.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    context = {
        'page': 'Success Order',
        'order': order,
    }
    return render(request, 'order_success.html', context)

from review.models import Review

def my_orders(request):
    user_check(request)
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items').order_by('-id')

    # CHECK REVIEW STATUS

    for order in orders:
        order.review_exists = Review.objects.filter(order=order,user=request.user).exists()

        review = Review.objects.filter(order=order,user=request.user).first()

        if review:
            order.review_exists = True
            order.review_id = review.id
        else:
            order.review_exists = False
            order.review_id = None

    context = {
        'page': 'My Orders',
        'orders': orders,
    }
    return render(request,'my_orders.html',context)
# Address Data Functions

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


# Order Tracking

def order_tracking(request, id):
    user_check(request)
    order = get_object_or_404(Order.objects.prefetch_related('order_items'), id=id, user=request.user)

    context = {
        'page': 'Tracking Order',
        'order': order
    }
    return render(request,'order_tracking.html',context)


def cancel_order(request, id):
    user_check(request)
    order = get_object_or_404(Order, id=id, user=request.user)
    if order.order_status in ['Pending', 'Preparing']:
        order.order_status = 'Cancelled'
        order.is_cancelled = True
        order.save()

    return redirect('/my_orders/')