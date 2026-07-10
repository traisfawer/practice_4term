from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/booking/', views.booking_create, name='booking_create'),
    path('api/contact/', views.contact_create, name='contact_create'),
    path('api/register/', views.register_view, name='register'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
]
