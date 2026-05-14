from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from orders.models import *
from django.contrib import messages

from review.models import Review, ReviewImage


# Create your views here.

@login_required(login_url='/accounts/login/')
def add_review(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)

    if order.order_status != 'Delivered':
        messages.error(request, 'You cannot add a review for this order at this time.')
        return redirect('my_orders')

    already_reviewed = Review.objects.filter(order = order, user = request.user).exists()

    if already_reviewed:
        messages.error(request, 'You already reviewed this order.')
        return redirect('my_orders')

    if request.method == 'POST':
        rating = request.POST['rating']
        review_message = request.POST['review_message']
        review_image = request.FILES.get('review_image')

        review = Review.objects.create(
            user = request.user,
            order = order,
            restaurant = order.restaurant,
            rating = rating,
            review_message = review_message,
        )

        if review_image:
            ReviewImage.objects.create(review = review, image = review_image)

        messages.success(request, 'Review Added Successfully ❤️')
        return redirect('my_orders')

    context = {
        'page' : 'Add Review',
        'order' : order,
    }
    return render(request, 'add_review.html', context)


@login_required(login_url='/accounts/login/')
def edit_review(request):
    context = {
        'page' : 'Edit Review'
    }
    return render(request, 'edit_review.html', context)


@login_required(login_url='/accounts/login/')
def delete_review(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review Deleted Successfully')
        return redirect('my_orders')

    context = {
        'page' : 'Delete Review',
        'review' : review
    }
    return render(request, 'delete_review.html', context)


@login_required(login_url='/accounts/login/')
def review_list(request):
    context = {
        'page' : 'Review List'
    }
    return render(request, 'review_list.html', context)
