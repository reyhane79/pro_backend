from django.contrib import admin

# Register your models here.
from shop.models import Order, OrderItem, OrderProduct, Wallet, Reply, Comment

admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(OrderProduct)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Reply)

