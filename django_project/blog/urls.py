from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='blog-home'),
    path('grafik/', views.grafik, name='blog-grafik'),
    path('yorumlar/', views.yorumlar, name='blog-yorumlar'),
    path('bos/', views.bos, name='blog-bos'),
    path('olumlu/', views.olumlu, name='blog-olumlu'),
    path('kategoriler/', views.kategoriler, name='blog-kategoriler')
]
