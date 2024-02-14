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
from django.conf import settings
from django.conf.urls.static import static
from .views import AppointmentView, AppointmentDetailView, UserAppointmentsView, AppointmentDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', views.LoginView.as_view()),
    path('user/logout/', views.LogoutView.as_view()),
    path('user/register/', views.RegisterView.as_view()),
    path('user/update/', views.UpdateUserView.as_view(), name='update-user'),
    path('users/', views.UserListView.as_view()),
    path('veterinaries/', views.VeterinaryListCreateView.as_view(), name='veterinary-list-create'),
    path('veterinary/<int:pk>/', views.VeterinaryDetailView.as_view(), name='veterinary-detail'),
    path('csrf/', views.GetCSRFToken.as_view()),
    path('reviews/', views.PostReview.as_view(), name='post_review'),
    path('appointments/', AppointmentView.as_view(), name='appointments'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/me/', UserAppointmentsView.as_view(), name='user-appointments'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
