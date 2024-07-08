from django.urls import path
from .views import home, check_out, add_product, add_to_cart, view_cart, orders

urlpatterns=[
    path('', home, name='home'),
    path('checkout/', check_out, name='checkout'),
    path('upload-product/',add_product, name='add_product'),
    path('add-t-cart/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('orders/', orders, name='orders'),
]