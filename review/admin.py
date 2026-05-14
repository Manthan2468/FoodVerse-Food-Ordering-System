from django.contrib import admin
from review.models import *

# Register your models here.

admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(ReviewLike)