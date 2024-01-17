from django.db import models

# Create your models here.

class ProductLocation(models.TextChoices):
    PRIVATE = 'private_box', 'Private Box'
    MEDICARE = 'medicare', 'Medicare'
    FOOD = 'food', 'Food'

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.category_name
    


class Product(models.Model):
    product_name = models.CharField(max_length=150)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    product_location = models.CharField(max_length=15, choices = ProductLocation.choices, default = ProductLocation.MEDICARE)
    stock = models.PositiveIntegerField(default = 0, blank=True, null=True)
    product_price = models.DecimalField(default=0, max_digits=19, decimal_places=4, null=True, blank=True,)
    product_vat = models.DecimalField(default=0, max_digits=19, decimal_places=4, null=True, blank=True, )
    product_discount = models.DecimalField(default=0, max_digits=19, decimal_places=4, null=True, blank=True,)
    product_barcode = models.CharField(max_length=50, unique= True, blank=True, null=True)
    
    def __str__(self):
        return self.product_name



    