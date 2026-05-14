from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Restaurant
from orders.models import Order

# Create your models here.

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_reviews')
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_reviews')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='restaurant_reviews')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='product_reviews', null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    review_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.rating} Star'


class ReviewImage(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE, related_name='review_images')
    image = models.ImageField(upload_to='review_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Review {self.review.id}"


class ReviewLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.ForeignKey(Review,on_delete=models.CASCADE, related_name='review_likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f'{self.user.username} liked Review {self.review.id}'