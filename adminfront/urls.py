# urls.py

from django.urls import path
from . import views
from .views import inscription_admin, connexion_admin, deconnexion_admin
from django.urls import path
from .views import (
    CategorieListView, CategorieCreateView, CategorieUpdateView, CategorieDeleteView,
    ProduitListView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView
)

urlpatterns = [
    path('', views.Admin_home, name='home_admin'),

    path('test', views.test, name='test'),
    path('admin/commandes/<int:commande_id>/mettre_a_jour/', views.mettre_a_jour_commande, name='mettre_a_jour_commande'),
    path('admin/commandes/<int:commande_id>/supprimer/', views.supprimer_commande, name='supprimer_commande'),
    path('admin/commandes/', views.commandes_admin, name='commandes_admin'),
    path('admin_index.html', views.admin_index, name='admin_index'),
    path('inscription/', views.inscription_admin, name='inscription_admin'),
    path('connexion/', views.connexion_admin, name='connexion_admin'),
    path('deconnexion/', views.deconnexion_admin, name='deconnexion_admin'),



    #gestion des produits et categorie
    # urls.py


    path('categories/', CategorieListView.as_view(), name='categorie_list'),
    path('categories/ajouter/', CategorieCreateView.as_view(), name='categorie_create'),
    path('categories/modifier/<int:pk>/', CategorieUpdateView.as_view(), name='categorie_update'),
    path('categories/supprimer/<int:pk>/', CategorieDeleteView.as_view(), name='categorie_delete'),
    
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/ajouter/', ProduitCreateView.as_view(), name='produit_create'),
    path('produits/modifier/<int:pk>/', ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/supprimer/<int:pk>/', ProduitDeleteView.as_view(), name='produit_delete'),


]









