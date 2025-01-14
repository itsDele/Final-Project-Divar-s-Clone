from django.contrib import admin
from django.urls import path, include
from .views import user_login, user_logout, create_advertising, edit_ad, product_detail, delete_advertisement, delete_image

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('advertisement/create/', create_advertising, name='create_advertisement'),
    path('advertisement/edit/<slug:slug>/', edit_ad, name='edit_ad'),  # Ensured this is defined
    path('advertisement/<slug:slug>/', product_detail, name='product_detail'),
    path('advertisement/delete/<int:id>/', delete_advertisement, name='delete_advertisement'),
    path('advertisement/delete_image/<int:id>/', delete_image, name='delete_image'),
]