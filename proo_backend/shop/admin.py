from django.contrib import admin

# Register your models here.
from shop.models import Order, OrderItem, OrderProduct

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(OrderItem)

