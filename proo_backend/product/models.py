from django.db import models

# Create your models here.
from users.models import Shop


class ProductCategory(models.Model):
    title = models.CharField(null=False, blank=False, unique=True, max_length=20)
    icon = models.ImageField(null=True, upload_to='./product/product images')


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=20)
    description = models.CharField(null=True, blank=False, max_length=50)
    price = models.FloatField(null=False, blank=False)
    image = models.ImageField(null=True, upload_to='./product/product images')
    stock = models.IntegerField(default=0, null=False)

