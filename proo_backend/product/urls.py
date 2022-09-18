from rest_framework.urls import path

from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('get_product/', views.get_product, name='get_product'),
    # path('edit_product/', ),
    # path('delete_product/')
]