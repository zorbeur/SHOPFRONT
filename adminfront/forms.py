from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Administrateur

class AdministrateurCreationForm(UserCreationForm):
    class Meta:
        model = Administrateur
        fields = ('nom', 'prenom', 'nomutilisateur', 'email', 'photo_de_profil')


#GESTION DES CATEGORIES ET PRODUITS
from django import forms
from .models import Categorie, Produit

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'image','description']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['categorie', 'nom', 'description', 'prix', 'quantite', 'image']
