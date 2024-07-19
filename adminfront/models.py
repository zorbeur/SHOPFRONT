from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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



#Gestion des fonctionnalites de notre liste deroulante Menus


from django.db import models
from django.utils.text import slugify

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



class Panier(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)
    commande = models.BooleanField(default=False)

    class Meta:
        unique_together = ('utilisateur', 'produit')

    def __str__(self):
        return f'{self.produit.nom} ({self.quantite}) dans le panier de {self.utilisateur.nomutilisateur}'

    def get_total_prix(self):
        return self.produit.prix * self.quantite

    def get_total_prix_panier(utilisateur):
        panier_items = Panier.objects.filter(utilisateur=utilisateur, commande=False)
        total = sum([item.get_total_prix() for item in panier_items])
        return total
    










