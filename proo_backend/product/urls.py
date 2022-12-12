from rest_framework.urls import path

from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('get_product/', views.get_product, name='get_product'),
    path('add_item_category/', views.add_item_category, name='add_item_category'),
    path('add_item/', views.add_item, name='add_item'),
    path('get_item_category/', views.get_item_category, name='get_item_category'),
    path('get_items/', views.get_items, name='get_items'),
    path('get_product_categories/', views.get_product_categories, name='get_product_categories'),
    path('change_product_info/', views.change_product_info, name='change_product_info'),

]
