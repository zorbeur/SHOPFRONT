from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index2, name='home2'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('profil/', views.profil, name='profil'),
    path('connexion/', views.connexion, name='connexion'),
    path('enregistrement/', views.enregistrement, name='enregistrement'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
