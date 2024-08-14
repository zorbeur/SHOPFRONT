# urls.py

from django.urls import path
from . import views
from django.conf.urls import handler404, handler500, handler403, handler400
from .views import afficher_notifications, creer_notification, marquer_comme_lu, supprimer_notification
from .views import liste_clients
from .views import inscription_admin, connexion_admin, deconnexion_admin
from django.urls import path
from .views import ajouter_modifier_livraison, afficher_livraison
from .views import (
    CategorieListView, CategorieCreateView, CategorieUpdateView, CategorieDeleteView,
    ProduitListView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView
)
handler400 = 'adminfront.views.custom_error_view'
handler403 = 'adminfront.views.custom_error_view'
handler404 = 'adminfront.views.custom_error_view'
handler500 = 'adminfront.views.custom_error_view'

urlpatterns = [
    path('notifications/', afficher_notifications, name='afficher_notifications'),
    path('notifications/creer/', creer_notification, name='creer_notification'),
    path('notifications/marquer_comme_lu/<int:notification_id>/', marquer_comme_lu, name='marquer_comme_lu'),
    path('notifications/supprimer/<int:notification_id>/', supprimer_notification, name='supprimer_notification'),
    path('', views.Admin_home, name='home_admin'),

    path('test', views.test, name='test'),
    path('clients/', liste_clients, name='liste_clients'),
    path('admin/commandes/<int:commande_id>/mettre_a_jour/', views.mettre_a_jour_commande, name='mettre_a_jour_commande'),
    path('admin/commandes/<int:commande_id>/supprimer/', views.supprimer_commande, name='supprimer_commande'),
    path('admin/commandes/', views.commandes_admin, name='commandes_admin'),
    path('admin_index.html', views.admin_index, name='admin_index'),
    path('inscription/', views.inscription_admin, name='inscription_admin'),
    path('connexion/', views.connexion_admin, name='connexion_admin'),
    path('deconnexion/', views.deconnexion_admin, name='deconnexion_admin'),



    #gestion des produits et categorie
    # urls.py

   

    path('livraison/<int:commande_id>/', afficher_livraison, name='afficher_livraison'),
    path('livraison/<int:commande_id>/edit/', ajouter_modifier_livraison, name='ajouter_modifier_livraison'),
    path('categories/', CategorieListView.as_view(), name='categorie_list'),
    path('categories/ajouter/', CategorieCreateView.as_view(), name='categorie_create'),
    path('categories/modifier/<int:pk>/', CategorieUpdateView.as_view(), name='categorie_update'),
    path('categories/supprimer/<int:pk>/', CategorieDeleteView.as_view(), name='categorie_delete'),
    
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/ajouter/', ProduitCreateView.as_view(), name='produit_create'),
    path('produits/modifier/<int:pk>/', ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/supprimer/<int:pk>/', ProduitDeleteView.as_view(), name='produit_delete'),


]









