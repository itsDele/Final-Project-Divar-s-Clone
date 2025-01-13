from django.urls import path, include
from .views import (
    MainPage,
    ad_detail_view,
    register,
    login_user,
    logout_user,
    add_ad,
    edit_ad,
    delete_ad,
    delete_photo,
    suggest_ads_template
)

urlpatterns = [
    path('', MainPage, name='home'),
    path('product/<slug:slug>/', ad_detail_view, name='product_detail'),
    path('signup/', register, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-ad/', add_ad, name='create_advertisement'),
    path('edit-ad/<slug:slug>/', edit_ad, name='edit_ad'),
    path('edit-ad/<slug:slug>/delete/', delete_ad, name='delete_advertisement'),
    path('delete_image/<int:photo_id>/', delete_photo, name='delete_image'),
    path('api/', include('Main.api.urls')),
    path('suggestions/', suggest_ads_template, name='advertisement_suggestions'),
]