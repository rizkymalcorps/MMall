from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
import datetime

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to="pic/%Y/%m/%d",default='no-image.png')
    price = models.DecimalField(decimal_places=2,max_digits=18,default=0)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey('Category')
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return "%s (%s)" % (self.title,self.brand.name)

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    STATUS_CART = (
        ('o', 'Order'),
        ('p', 'Pending'),
        ('d', 'Delivered'),
    )

    customer_name = models.CharField(max_length=255,default="", verbose_name="Customer Name")
    customer_address = models.CharField(max_length=255,default="", verbose_name="Customer Address")
    customer_email = models.EmailField(blank=False, default="", verbose_name="Customer Email")
    customer_phone = models.CharField(max_length=12,default="",verbose_name="Customer Phone")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    status = models.CharField(max_length=1 ,choices=STATUS_CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s #order_%d " % (self.customer_name,self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()


    def __str__(self):
        return "%s" % (self.product.title)
