from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='reviewPro-home'),
    path('grafik/', views.grafik, name='reviewPro-grafik'),
    path('yorumlar/', views.yorumlar, name='reviewPro-yorumlar'),
    path('yorumlar/hotel/', views.yorumlarhotel, name='reviewPro-yorumlar-hotel'), #yeni satır
    path('yorumlar/staff/', views.yorumlarstaff, name='reviewPro-yorumlar-staff'), #yeni satır
    path('yorumlar/location/', views.yorumlarlocation, name='reviewPro-yorumlar-location'), #yeni satır
    path('yorumlar/room/', views.yorumlarroom, name='reviewPro-yorumlar-room'), #yeni satır
    path('yorumlar/breakfast/', views.yorumlarbreakfast, name='reviewPro-yorumlar-breakfast'), #yeni satır
    path('yorumlar/bed/', views.yorumlarbed, name='reviewPro-yorumlar-bed'), #yeni satır
    path('yorumlar/service/', views.yorumlarservice, name='reviewPro-yorumlar-service'), #yeni satır
    path('yorumlar/bathroom/', views.yorumlarbathroom, name='reviewPro-yorumlar-bathroom'), #yeni satır
    path('yorumlar/view/', views.yorumlarview, name='reviewPro-yorumlar-view'), #yeni satır
    path('yorumlar/food/', views.yorumlarfood, name='reviewPro-yorumlar-food'), #yeni satır
    path('yorumlar/restaurant/', views.yorumlarrestaurant, name='reviewPro-yorumlar-restaurant'), #yeni satır
    
    path('kategoriler/', views.kategoriler, name='reviewPro-kategoriler')
]
