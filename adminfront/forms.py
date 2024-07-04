from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Administrateur

class AdministrateurCreationForm(UserCreationForm):
    class Meta:
        model = Administrateur
        fields = ('nom', 'prenom', 'nomutilisateur', 'email', 'photo_de_profil')


