from secrets import choice

from django.db import models
import uuid

# Create your models here.

# DRY => Do not repeat your self to use BaseModel
class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True)
    creat_date = models.DateTimeField(auto_created=True)
    updated_date = models.DateTimeField(auto_created=True)

    class Meta:
        abstract = True # base class is act as only class not model when we use abstract

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)
    product_actual_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.0)

class Product_MetaInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_meta_info')
    product_measuring = models.CharField(max_length = 100, choices = (("KG","KG"),("L","L"),("ML","ML")), default=0,null=True,blank=True)
    quantity = models.CharField(default=0,null=True,blank=True)
    is_restrict = models.BooleanField(default=False)
    restrict_quantity = models.IntegerField(default=0,null=True,blank=True)

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    product_images = models.ImageField(upload_to = 'products/%Y/%m/%d')
