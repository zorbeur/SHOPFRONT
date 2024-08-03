from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.text import slugify
from django.utils import timezone

class AdministrateurManager(BaseUserManager):
    def create_user(self, nom, prenom, nomutilisateur, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être renseignée")
        if not nomutilisateur:
            raise ValueError("Le nom d'utilisateur doit être renseigné")
        
        email = self.normalize_email(email)
        user = self.model(
            nom=nom,
            prenom=prenom,
            nomutilisateur=nomutilisateur,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        Cart.objects.create(utilisateur=user)  # Création du panier
        return user

    def create_superuser(self, nom, prenom, nomutilisateur, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(nom, prenom, nomutilisateur, email, password, **extra_fields)

class Administrateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    nomutilisateur = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    photo_de_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrateur_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrateur_set',
        blank=True
    )

    objects = AdministrateurManager()

    USERNAME_FIELD = 'nomutilisateur'
    REQUIRED_FIELDS = ['nom', 'prenom', 'email']

    def __str__(self):
        return self.nomutilisateur

    def get_full_name(self):
        return f'{self.prenom} {self.nom}'

    def get_short_name(self):
        return self.prenom

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/')
    quantite = models.IntegerField(default=0)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Cart(models.Model):
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart',
        null=True,  # Rendre le champ nullable
        blank=True  # Permettre les valeurs vides dans les formulaires
    )
    created_at = models.DateTimeField(default=timezone.now)  # Ajout de la valeur par défaut

    def __str__(self):
        return f'Cart for {self.utilisateur.nomutilisateur}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantite} of {self.produit.nom}'

class Commande(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    adresse_livraison = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    etat_commande = models.CharField(max_length=50, choices=[
        ('EN_ATTENTE', 'En attente'),
        ('EN_TRAITEMENT', 'En traitement'),
        ('EXPEDIE', 'Expédié'),
        ('LIVRE', 'Livré'),
    ], default='EN_ATTENTE')

    def __str__(self):
        return f"Commande {self.id} - {self.utilisateur.nomutilisateur}"



class ElementCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='elements')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Produit {self.produit.nom} - Quantité {self.quantite}"

    @property
    def prix_total(self):
        return self.quantite * self.prix_unitaire
