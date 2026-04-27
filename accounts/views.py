from django.contrib.auth import authenticate, login as log
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import *

# Create your views here.

def register(request):

    if request.method == 'POST':
        email =request.POST['email']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('register')

        if Profile.objects.filter(phone_number=phone_number).exists():
            messages.error(request,'Phone number already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, phone_number=phone_number)

        messages.success(request,'User created successfully')
        return redirect('login')

    context = {
        'page': 'Register'
    }
    return render(request,'register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_data = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,'Email does not exist')
            return redirect('login')

        user = authenticate(request, username=user_data.username, password=password)

        if user is None:
            messages.error(request,'Invalid username or password!')
            return redirect('login')
        else:
            log(request, user) # It set auto session after this function and we can access data like request.user.username
            return redirect('home')

    context = {'page': 'Login'}
    return render(request,'login.html', context)
