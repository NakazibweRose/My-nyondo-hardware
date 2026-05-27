from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', lambda request: redirect('login')), # Redirect the root URL to the login page
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
]
