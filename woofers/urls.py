"""
URL configuration for woofers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from woofers import views
from .views import UpdateUserView, GetCSRFToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', views.LoginView.as_view()),
    path('user/logout/', views.LogoutView.as_view()),
    path('user/user/', views.current_user, name='current-user'),
    path('user/user/update/', UpdateUserView.as_view(), name='update-user'),
    path('user/register/', views.RegisterView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('veterinaries/', views.VeterinaryListCreateView.as_view(), name='veterinary-list-create'),
    path('veterinary/<int:pk>/', views.VeterinaryDetailView.as_view(), name='veterinary-detail'),
    path('csrf/', GetCSRFToken.as_view()),
]
