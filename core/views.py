from django.shortcuts import render, redirect
from django.contrib.auth import logout
from products.models import *
from orders.models import *

# Create your views here.

def home(request):
    context = {
        'page': 'Home',
        'categories': Category.objects.all()[0:7],
        'popular_products': Product.objects.filter(is_popular=True).order_by('-rating')[0:3],
        'restaurant': Restaurant.objects.all().order_by('-rating')[0:3],
    }
    Product.objects.filter(rating__gt=4.5).update(is_popular=True)
    return render(request,'home.html', context)

def logout_page(request):
    logout(request)
    return redirect('/login/')

def about(request):
    context = {
        'page': 'About Us',
    }
    return render(request, 'about.html', context)


def contact(request):
    context = {
        'page': 'Contact Us',
    }
    return render(request, 'contact.html', context)

def global_data(request):
    count_data = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count_data = CartItem.objects.filter(cart=cart).select_related('product').count()

    return {
        'number_of_cart_items': count_data,
    }