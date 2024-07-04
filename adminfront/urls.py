# urls.py

from django.urls import path
from . import views
from .views import inscription_admin, connexion_admin, deconnexion_admin
urlpatterns = [
    path('', views.Admin_home, name='home_admin'),

    path('admin_index.html', views.admin_index, name='admin_index'),


    path('inscription/', views.inscription_admin, name='inscription_admin'),
    path('connexion/', views.connexion_admin, name='connexion_admin'),
    path('deconnexion/', views.deconnexion_admin, name='deconnexion_admin'),
   
]









