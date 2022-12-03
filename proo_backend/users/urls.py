from rest_framework.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('get_shop_list/', views.get_shop_list, name='get_shop_list'),
    path('get_info/', views.get_info, name='get_info'),

]
