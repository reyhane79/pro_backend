from django.contrib import admin

# Register your models here.
from users.models import CustomUser, Customer, Shop

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Shop)
