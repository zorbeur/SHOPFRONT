from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import update_cart_item, delete_cart_item, ajouter_au_panier, cart
from .views import paiement, process_payment

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index2, name='home2'),
    path('shop/', views.shop, name='shop'),
    path('commande-status/<int:commande_id>/', views.commande_status, name='commande_status'),





    path('merci/<int:commande_id>/', views.merci, name='merci'),
    path('paiement/', paiement, name='paiement'),
    path('process_payment/', process_payment, name='process_payment'),




    path('panier/', cart, name='cart'),
    path('update-cart-item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('ajouter-au-panier/<int:produit_id>/', ajouter_au_panier, name='ajouter_au_panier'),

    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('profil/', views.profil, name='profil'),
    path('connexion/', views.connexion, name='connexion'),
    path('enregistrement/', views.enregistrement, name='enregistrement'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ajoutez cette ligne pour servir les fichiers du dossier 'categorie'
urlpatterns += static('/categorie/', document_root=settings.CATEGORIE_ROOT)