from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('checkout/', views.check_out, name='checkout'),
    path('upload-product/',views.add_product, name='add_product'),
    path('add-t-cart/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('orders/', views.orders, name='orders'),
    path('create-room/<str:uuid>/', views.create_room, name='create_room'),
    path('manage-room/', views.manage_rooms, name='manage_rooms'),
    path('single-room/<str:uuid>/', views.single_room, name='single_room'),
]