from django.contrib import admin

# Register your models here.
from shop.models import Order, OrderItem, OrderProduct, Wallet

admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(OrderProduct)
admin.site.register(OrderItem)

