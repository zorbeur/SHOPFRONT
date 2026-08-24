from django.urls import path
from . import views

urlpatterns = [
    # Tableau de bord
    path('', views.Admin_home, name='home_admin'),
    path('dashboard/', views.admin_index, name='admin_index'),
    path('admin_index.html', views.admin_index, name='admin_index_legacy'),

    # Authentification
    path('connexion/', views.connexion_admin, name='connexion_admin'),
    path('deconnexion/', views.deconnexion_admin, name='deconnexion_admin'),
    path('inscription/', views.inscription_admin, name='inscription_admin'),

    # Catégories
    path('categories/', views.CategorieListView.as_view(), name='categorie_list'),
    path('categories/ajouter/', views.CategorieCreateView.as_view(), name='categorie_create'),
    path('categories/modifier/<int:pk>/', views.CategorieUpdateView.as_view(), name='categorie_update'),
    path('categories/supprimer/<int:pk>/', views.CategorieDeleteView.as_view(), name='categorie_delete'),

    # Produits
    path('produits/', views.ProduitListView.as_view(), name='produit_list'),
    path('produits/ajouter/', views.ProduitCreateView.as_view(), name='produit_create'),
    path('produits/modifier/<int:pk>/', views.ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/supprimer/<int:pk>/', views.ProduitDeleteView.as_view(), name='produit_delete'),

    # Commandes
    path('commandes/', views.commandes_admin, name='commandes_admin'),
    path('admin/commandes/', views.commandes_admin, name='commandes_admin_legacy'),
    path('commandes/<int:commande_id>/mettre_a_jour/', views.mettre_a_jour_commande, name='mettre_a_jour_commande'),
    path('admin/commandes/<int:commande_id>/mettre_a_jour/', views.mettre_a_jour_commande, name='mettre_a_jour_commande_legacy'),
    path('commandes/<int:commande_id>/supprimer/', views.supprimer_commande, name='supprimer_commande'),
    path('admin/commandes/<int:commande_id>/supprimer/', views.supprimer_commande, name='supprimer_commande_legacy'),

    # Livraisons
    path('livraisons/', views.liste_livraisons, name='liste_livraisons'),
    path('livraison/<int:commande_id>/', views.afficher_livraison, name='afficher_livraison'),
    path('livraison/<int:commande_id>/edit/', views.ajouter_modifier_livraison, name='ajouter_modifier_livraison'),

    # Clients / Utilisateurs
    path('clients/', views.liste_clients, name='liste_clients'),

    # Notifications
    path('notifications/', views.afficher_notifications, name='afficher_notifications'),
    path('notifications/creer/', views.creer_notification, name='creer_notification'),
    path('notifications/marquer_comme_lu/<int:notification_id>/', views.marquer_comme_lu, name='marquer_comme_lu'),
    path('notifications/supprimer/<int:notification_id>/', views.supprimer_notification, name='supprimer_notification'),
]

