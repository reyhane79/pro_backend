from rest_framework.urls import path
from . import views

urlpatterns = [
    path('add_order_product/', views.add_order_product, name='add_order_product'),
    path('add_order_item/', views.add_order_item, name='add_order_item')

]
