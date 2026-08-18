
from django.contrib import admin
from .models import Produit, Categorie, Livraison

@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = ('commande', 'date_livraison', 'adresse_livraison', 'statut')
    list_filter = ('statut',)
    search_fields = ('commande__id', 'adresse_livraison')

admin.site.register(Produit)
admin.site.register(Categorie)





