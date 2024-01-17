from django.contrib import admin

from file_upload.models import (
    Category,
    Product
)

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name', 'product_category', 'product_location', 'product_price', 'product_vat', 'product_discount', 'product_barcode', )
