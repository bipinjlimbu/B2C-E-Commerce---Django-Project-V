from django.urls import path
from .views.auth_view import login_view, logout_view, register_view
from .views.main_view import home_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.brand_view import add_brand_view, edit_brand_view, delete_brand_view
from .views.product_view import products_view, add_product_view, edit_product_view, product_toggle_status_view, delete_product_view, product_detail_view
from .views.wishlist_view import wishlist_toggle_view, wishlist_view, remove_from_wishlist_view
from .views.cart_view import add_to_cart_view, cart_view, increase_cart_item_quantity_view, decrease_cart_item_quantity_view
from .views.dashboard import admin_dashboard_view, customer_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:profile_id>/', delete_profile_view, name='delete_profile'),
    path('brands/add/', add_brand_view, name='add_brand'),
    path('brands/edit/<int:brand_id>/', edit_brand_view, name='edit_brand'),
    path('brands/delete/<int:brand_id>/', delete_brand_view, name='delete_brand'),
    path('products/', products_view, name='products'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('products/edit/<int:product_id>/', edit_product_view, name='edit_product'),
    path('products/toggle-status/<int:product_id>/', product_toggle_status_view, name='product_toggle_status'),
    path('products/delete/<int:product_id>/', delete_product_view, name='delete_product'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('products/wishlist/remove/<int:product_id>/', remove_from_wishlist_view, name='remove_from_wishlist'),
    path('products/wishlist-toggle/<int:product_id>/', wishlist_toggle_view, name='wishlist_toggle'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/increase/<int:cart_item_id>/', increase_cart_item_quantity_view, name='increase_cart_item_quantity'),
    path('cart/decrease/<int:cart_item_id>/', decrease_cart_item_quantity_view, name='decrease_cart_item_quantity'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]