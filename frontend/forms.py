from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    nom = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre nom de famille',
        }),
        label="Nom"
    )
    prenom = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre prénom',
        }),
        label="Prénom"
    )
    nomutilisateur = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': "Nom d'utilisateur unique",
        }),
        label="Nom d'utilisateur"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'nom@exemple.com',
        }),
        label="Adresse email"
    )
    numero_de_telephone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '+228 90 00 00 00',
        }),
        label="Numéro de téléphone"
    )

    class Meta:
        model = User
        fields = ['nomutilisateur', 'prenom', 'nom', 'email', 'numero_de_telephone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre compte.")
        return email

    def clean_nomutilisateur(self):
        nomutilisateur = self.cleaned_data.get('nomutilisateur')
        if User.objects.filter(nomutilisateur=nomutilisateur).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return nomutilisateur

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': "Nom d'utilisateur",
            'autofocus': True,
        }),
        label="Nom d'utilisateur"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Mot de passe',
        }),
        label="Mot de passe"
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'numero_de_telephone', 'photo_de_profil']
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'numero_de_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_de_profil': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    adresse = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Rue des Palmiers, Quartier Tokoin',
        }),
        label="Adresse de livraison"
    )
    ville = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Lomé',
        }),
        label="Ville"
    )
    code_postal = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 00228',
        }),
        label="Code postal (optionnel)"
    )
    pays = forms.CharField(
        max_length=100,
        initial='Togo',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Togo',
        }),
        label="Pays"
    )
    telephone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: +228 90 00 00 00',
        }),
        label="Numéro de téléphone pour la livraison"
    )
    methode_paiement = forms.ChoiceField(
        choices=[
            ('LIVRAISON', 'Paiement à la livraison (Espèces ou Mobile Money)'),
            ('TMONEY', 'T-Money (Togocom)'),
            ('FLOOZ', 'Flooz (Moov Africa)'),
            ('CARTE', 'Carte bancaire (Visa / Mastercard)'),
        ],
        initial='LIVRAISON',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Mode de règlement"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Instructions de livraison spécifiques (facultatif)...',
        }),
        label="Notes de commande"
    )

class ContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom complet',
        }),
        label="Nom complet"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre adresse email',
        }),
        label="Email"
    )
    sujet = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Objet de votre message',
        }),
        label="Sujet"
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Écrivez votre message ici...',
        }),
        label="Message"
    )
