# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),


    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),


    path('profil/', views.profil, name='profil'),
    path('connexion/', views.connexion, name='connexion'),
    path('enregistrement/', views.enregistrement, name='enregistrement'),
]
