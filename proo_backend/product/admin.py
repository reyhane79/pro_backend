from django.contrib import admin

# Register your models here.
from product.models import Product, ProductCategory, ItemCategory, Item

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ItemCategory)
admin.site.register(Item)
