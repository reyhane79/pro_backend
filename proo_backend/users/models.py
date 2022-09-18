from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.manager import CustomUserManager

gender_choices = [
    (1, 'مرد'),
    (2, 'زن')
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(null=False, blank=False, max_length=11, unique=True)
    email = models.CharField(null=True, unique=True, max_length=50)
    name = models.CharField(max_length=50, null=True, blank=False)

    is_visible = models.BooleanField(default=True)
    date_joint = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_sailor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(choices=gender_choices, max_length=3)
    birthday = models.DateField(null=True, blank=False)


class Shop(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='بدون نام', null=False, blank=False)
    address = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='./users/logo/')
    delivery_cost = models.FloatField(default=0)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    score = models.FloatField(default=0)








