from django.contrib import admin

from orders.models import *

# Register your models here.

admin.site.register(Order)
admin.site.register(DeliveryAddress)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)