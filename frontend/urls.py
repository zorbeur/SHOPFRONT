from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index2, name='home2'),
    path('shop/', views.shop, name='shop'),

    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.afficher_panier, name='panier'),
    path('supprimer_du_panier/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('modifier_quantite/<int:produit_id>/<str:operation>/', views.modifier_quantite, name='modifier_quantite'),
    
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
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ajoutez cette ligne pour servir les fichiers du dossier 'categorie'
urlpatterns += static('/categorie/', document_root=settings.CATEGORIE_ROOT)