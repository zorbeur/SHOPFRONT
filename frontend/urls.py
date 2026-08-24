from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques principales
    path('', views.index, name='home'),
    path('home/', views.index2, name='home2'),
    path('shop/', views.shop, name='shop'),
    path('promotions/', views.promotions, name='promotions'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),

    # Détail Produit
    path('produit/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produit/<slug:slug>/', views.produit_detail, name='produit_detail_slug'),

    # Favoris / Wishlist
    path('favoris/', views.wishlist, name='wishlist'),
    path('favoris/toggle/<int:produit_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # Pages d'Aide & Informations Légales
    path('suivi-commande/', views.suivi_commande_public, name='suivi_commande_public'),
    path('faq/', views.faq, name='faq'),
    path('conditions-livraison/', views.conditions_livraison, name='conditions_livraison'),
    path('cgv/', views.conditions_livraison, name='cgv'),
    path('confidentialite/', views.confidentialite, name='confidentialite'),
    path('mentions-legales/', views.confidentialite, name='mentions_legales'),

    # Panier & Commande
    path('panier/', views.cart, name='cart'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('paiement/', views.paiement, name='paiement'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('merci/<int:commande_id>/', views.merci, name='merci'),
    path('commande-status/<int:commande_id>/', views.commande_status, name='commande_status'),

    # Utilisateur & Authentification
    path('profil/', views.profil, name='profil'),
    path('connexion/', views.connexion, name='connexion'),
    path('login/', views.connexion, name='login'),
    path('enregistrement/', views.enregistrement, name='enregistrement'),
    path('signup/', views.enregistrement, name='signup'),
    path('activation-en-attente/', views.activation_en_attente, name='activation_en_attente'),
    path('activer-compte/<str:uidb64>/<str:token>/', views.activer_compte, name='activer_compte'),
    path('renvoyer-activation/', views.renvoyer_activation, name='renvoyer_activation'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('logout/', views.deconnexion, name='logout'),
]
