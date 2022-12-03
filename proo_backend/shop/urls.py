from rest_framework.urls import path
from . import views

urlpatterns = [
    path('add_order_product/', views.add_order_product, name='add_order_product'),
    path('add_order_item/', views.add_order_item, name='add_order_item'),
    path('get_orders/', views.get_orders, name='get_orders'),
    path('finish_order/', views.finish_order, name='finish_order'),
    path('change_order_stage_by_shop/', views.change_order_stage_by_shop, name='change_order_stage_by_shop'),
    path('change_order_stage_by_customer/', views.change_order_stage_by_customer, name='change_order_stage_by_customer'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('remove_order_product/', views.remove_order_product, name='remove_order_product'),
    path('remove_order_item/', views.remove_order_item, name='remove_order_item'),

]
