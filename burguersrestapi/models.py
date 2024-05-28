from django.db import models

PRODUCTTYPE_CHOICES = {"D":"Drink","B":"Burguer"}
ORDERTYPE_CHOICES = {"D":"Delivery","P":"Pickup"}

# Create your models here.
class Ingredient(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ['created']

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    productType = models.CharField(choices=PRODUCTTYPE_CHOICES, max_length=10)
    price = models.DecimalField(max_digits=4,decimal_places=2,blank=False, default=0)
    name = models.CharField(max_length=100, blank=False, default='')
    description = models.CharField(max_length=100, blank=False, default='')
    image = models.ImageField(upload_to='products-img/')
    
    class Meta:
        ordering = ['created']

class Burger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    refProduct = models.OneToOneField(Product,on_delete=models.CASCADE, primary_key=True)
    ingredients = models.ManyToManyField(Ingredient)

    class Meta:
        ordering = ['created']

class Drink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    refProduct = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ['created']

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    orderDayHour = models.DateTimeField(auto_now_add=False)
    orderType = models.CharField(choices=ORDERTYPE_CHOICES, default='P',max_length=1)
    adress = models.CharField(max_length=100)
    info = models.CharField(max_length=100, blank=True)
    products = models.ManyToManyField(Product)
    
    class Meta:
        ordering = ['created']
        