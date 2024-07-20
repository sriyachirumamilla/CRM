# common/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sales/', views.sales_view, name='sales'),
    path('products/', views.product_list, name='product_list'),
]
