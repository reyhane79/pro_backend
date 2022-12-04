from django.db import models

# Create your models here.
from product.models import Product, Item
from users.models import CustomUser

stages = [
    (1, 'تکمیل نشده'),
    (2, 'در انتظار تایید فروشگاه'),
    (3, 'در حال آماده سازی'),
    (4, 'در حال ارسال'),
    (5, 'دریافت شده'),
    (6, 'دریافت نشده'),
]


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    credit = models.FloatField(default=500000, null=False, blank=False)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False)
    tracking_code = models.CharField(blank=False, max_length=100, null=True)
    stage = models.CharField(choices=stages, default=1, max_length=25)
    minimum_delivery_time = models.DateTimeField(null=True, blank=False)
    max_delivery_time = models.DateTimeField(null=True, blank=False)
    price = models.FloatField(default=0)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


