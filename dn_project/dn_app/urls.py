from django.urls import path
from .views.auth_view import login_view, logout_view, register_view
from .views.main_view import home_view
from .views.profile_view import profile_view, edit_profile_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
]