from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='blog-home'),
    path('grafik/', views.grafik, name='blog-grafik'),
    path('yorumlar/', views.yorumlar, name='blog-yorumlar'),
    path('yorumlar/hotel/', views.yorumlarhotel, name='blog-yorumlar-hotel'), #yeni satır
    path('yorumlar/staff/', views.yorumlarstaff, name='blog-yorumlar-staff'), #yeni satır
    path('yorumlar/location/', views.yorumlarlocation, name='blog-yorumlar-location'), #yeni satır
    path('yorumlar/room/', views.yorumlarroom, name='blog-yorumlar-room'), #yeni satır
    path('yorumlar/breakfast/', views.yorumlarbreakfast, name='blog-yorumlar-breakfast'), #yeni satır
    path('yorumlar/bed/', views.yorumlarbed, name='blog-yorumlar-bed'), #yeni satır
    path('yorumlar/service/', views.yorumlarservice, name='blog-yorumlar-service'), #yeni satır
    path('yorumlar/bathroom/', views.yorumlarbathroom, name='blog-yorumlar-bathroom'), #yeni satır
    path('yorumlar/view/', views.yorumlarview, name='blog-yorumlar-view'), #yeni satır
    path('yorumlar/food/', views.yorumlarfood, name='blog-yorumlar-food'), #yeni satır
    path('yorumlar/restaurant/', views.yorumlarrestaurant, name='blog-yorumlar-restaurant'), #yeni satır
    
    path('kategoriler/', views.kategoriler, name='blog-kategoriler')
]
