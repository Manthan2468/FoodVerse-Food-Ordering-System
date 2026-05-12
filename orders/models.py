from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Restaurant


# ================= CART =================

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name

# ================= ADDRESS =================

class DeliveryAddress(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


# ================= ORDER =================

class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Preparing','Preparing'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('COD','Cash On Delivery'),
        ('Online','Online Payment'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    address = models.ForeignKey(DeliveryAddress,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6,decimal_places=2,default=40)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES,default='COD')
    order_status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"



# ================= ORDER ITEMS =================

class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product.name