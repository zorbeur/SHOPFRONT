from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Administrateur

class AdministrateurCreationForm(UserCreationForm):
    class Meta:
        model = Administrateur
        fields = ('nom', 'prenom', 'nomutilisateur', 'email', 'photo_de_profil')


# forms.py
from django import forms
from .models import Categorie, Produit

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'image']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'image', 'quantite', 'categorie']

from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['utilisateur', 'date_commande', 'total', 'adresse_livraison', 'code_postal', 'ville', 'pays', 'etat_commande']
        widgets = {
            'date_commande': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
