from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import CartItem, Cart
from products.models import Category, Product, Restaurant
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def product_list(request, id):
    products = Product.objects.filter(category=id)
    category = Category.objects.get(id=id)
    context = {
        'page' : 'Product List',
        'products' : products,
        'category_name' : category.name,
    }
    return render(request,'product_list.html', context)

@login_required(login_url='/login/')
def category(request):
    categories = Category.objects.all()
    context = {
        'page' : 'Category',
        'categories' : categories,
    }
    return render(request,'category.html', context)

@login_required(login_url='/login/')
def popular_dishes(request):
    dishes = Product.objects.filter(is_popular=True).order_by('-rating')
    context = {
        'page' : 'Popular Dishes',
        'dishes' : dishes,
    }
    return render(request,'popular_dishes.html', context)


@login_required(login_url='/login/')
def restaurant(request):
    restaurants = Restaurant.objects.all()
    context = {
        'page' : 'Restaurants',
        'restaurant' : restaurants,
    }
    return render(request, 'restaurants.html', context)


@login_required(login_url='/login/')
def menu(request):
    menus = Product.objects.all().order_by('-rating')
    context = {
        'page' : 'Menu',
        'menu' : menus,
    }
    return render(request, 'menu.html', context)


@login_required(login_url='/login/')
def view_menu(request, id):
    restaurants_data = get_object_or_404(Restaurant, id=id)
    menu_data = Product.objects.filter(restaurant=restaurants_data).order_by('-rating')
    context = {
        'page' : 'Restaurant Menu',
        'restaurant' : restaurants_data,
        'menu' : menu_data
    }
    return render(request, 'view_menu.html', context)

def add_item_cart(request, id):
    product_data = get_object_or_404(Product, id=id)

    if product_data.is_available == False:
        messages.error(request, 'Product is not available')
        return redirect('/product_list/4')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product=product_data)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(f'/product_list/{product_data.category.id}')
