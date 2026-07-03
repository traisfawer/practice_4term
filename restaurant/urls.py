from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/booking/', views.booking_create, name='booking_create'),
]
