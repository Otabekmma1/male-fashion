from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('shop/category/<int:category_id>/', shop, name='shop_by_category'),
    path('shop/size/<int:size_id>/', shop, name='shop_by_size'),
    path('blog/', blog, name='blog'),
    path('blog-detail/', blog_detail, name='blog_detail'),
    path('contact/', contact, name='contact'),
    path('product-detail/<slug>/', product_detail_by_slug, name='product_detail'),
    path('sorting/<slug:key_name>/', SortingProductList.as_view(), name='sorting'),
    path('rate/<int:product_id>/<int:rating>/', rate),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('delete-product/<int:product_id>/', delete_product_from_cart, name='delete_product'),
    path('check/', check, name='check'),
    path('payment/', create_checkout_sessions, name='pay'),

    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    path('profile/', user_profile, name='profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),



]