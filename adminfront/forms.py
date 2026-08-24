from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Administrateur, Categorie, Produit, Commande, Livraison, Notification

class AdministrateurCreationForm(UserCreationForm):
    class Meta:
        model = Administrateur
        fields = ('prenom', 'nom', 'nomutilisateur', 'email', 'numero_de_telephone', 'photo_de_profil', 'is_staff')
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'nomutilisateur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemple.com'}),
            'numero_de_telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+228 90 00 00 00'}),
            'photo_de_profil': forms.FileInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description de la catégorie...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'prix', 'quantite', 'description', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ex: 25000', 'step': '0.01'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ex: 15'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['utilisateur', 'total', 'etat_commande', 'adresse_livraison', 'ville', 'code_postal', 'pays']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'etat_commande': forms.Select(attrs={'class': 'form-select'}),
            'adresse_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['statut', 'adresse_livraison', 'ville', 'code_postal', 'pays', 'date_livraison']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'adresse_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'date_livraison': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['utilisateur', 'message']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Message de la notification...'}),
        }
