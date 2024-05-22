from django.contrib import admin
from django.urls import path
from . import views as v1

urlpatterns = [
    path('',v1.home,name="home"),
    path('register/',v1.register,name="register"),
    path('login/',v1.login_page,name="login"),
    path('logout/',v1.logout_page,name="logout"),
    path('addtocart', v1.add_to_cart, name='add_to_cart'),
    path('remove_cart/<str:cid>',v1.remove_cart,name='remove_cart'),
    path('cart',v1.cart_page,name='cart'),
    path('fav',v1.fav_page,name='fav_page'),
    path('fav_view_page',v1.fav_view_page,name='fav_view_page'),
    path('remove_fav/<str:fid>',v1.remove_fav,name="remove_fav"),
    path('remove_cart/<str:cid>',v1.remove_cart,name="remove_cart"),
    path('collections/',v1.collections,name="collections"),
    path('collections/<str:name>/', v1.collectionview, name='collections'),
    path('collections/<str:cname>/<str:pname>', v1.product_details, name='product_details')
]
