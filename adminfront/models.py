from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.text import slugify
from django.utils import timezone

class AdministrateurManager(BaseUserManager):
    def create_user(self, nomutilisateur, email, password=None, nom="", prenom="", **extra_fields):
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
        Cart.objects.get_or_create(utilisateur=user)  # Création sécurisée du panier
        return user

    def create_superuser(self, nomutilisateur, email, password=None, nom="", prenom="", **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(nomutilisateur, email, password, nom=nom, prenom=prenom, **extra_fields)

class Administrateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    nomutilisateur = models.CharField(max_length=50, unique=True, verbose_name="Nom d'utilisateur")
    email = models.EmailField(unique=True, verbose_name="Email")
    photo_de_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True, verbose_name="Photo de profil")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Équipe administrative")
    numero_de_telephone = models.CharField(max_length=30, default='+22890912367', blank=True, verbose_name="Numéro de téléphone")
    date_inscription = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    email_verifie = models.BooleanField(default=True, verbose_name="Email vérifié")

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

    class Meta:
        verbose_name = "Utilisateur / Administrateur"
        verbose_name_plural = "Utilisateurs / Administrateurs"
        ordering = ['-id']

    def __str__(self):
        return f"{self.nomutilisateur} ({self.get_full_name()})"

    @property
    def username(self):
        return self.nomutilisateur

    @username.setter
    def username(self, value):
        self.nomutilisateur = value

    def get_full_name(self):
        return f'{self.prenom} {self.nom}'.strip() or self.nomutilisateur

    def get_short_name(self):
        return self.prenom or self.nomutilisateur

class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image de catégorie")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nom) or 'categorie'
            slug = base_slug
            counter = 1
            while Categorie.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    @property
    def total_produits(self):
        return self.produit_set.count()

class Produit(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description détaillée")
    prix = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix (FCFA)")
    image = models.ImageField(upload_to='produits/', verbose_name="Image du produit")
    quantite = models.IntegerField(default=0, verbose_name="Quantité en stock")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name="Catégorie")
    slug = models.SlugField(unique=True, blank=True)
    date_ajout = models.DateTimeField(default=timezone.now, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-date_ajout', '-id']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nom) or 'produit'
            slug = base_slug
            counter = 1
            while Produit.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    @property
    def en_stock(self):
        return self.quantite > 0

class Cart(models.Model):
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_str = self.utilisateur.nomutilisateur if self.utilisateur else "Anonyme"
        return f'Panier pour {user_str}'

    @property
    def total(self):
        return sum(item.total_prix for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantite} x {self.produit.nom}'

    @property
    def total_prix(self):
        return self.quantite * self.produit.prix

class Commande(models.Model):
    ETAT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_TRAITEMENT', 'En traitement'),
        ('EXPEDIE', 'Expédié'),
        ('LIVRE', 'Livré'),
        ('ANNULE', 'Annulé'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(default=timezone.now, verbose_name="Date de commande")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total (FCFA)")
    adresse_livraison = models.CharField(max_length=255, verbose_name="Adresse")
    code_postal = models.CharField(max_length=20, blank=True, verbose_name="Code postal")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, default='Togo', verbose_name="Pays")
    etat_commande = models.CharField(max_length=50, choices=ETAT_CHOICES, default='EN_ATTENTE', verbose_name="État de la commande")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande', '-id']

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.nomutilisateur} ({self.total} FCFA)"

    @property
    def status_badge_class(self):
        badges = {
            'EN_ATTENTE': 'warning',
            'EN_TRAITEMENT': 'info',
            'EXPEDIE': 'primary',
            'LIVRE': 'success',
            'ANNULE': 'danger',
        }
        return badges.get(self.etat_commande, 'secondary')

class ElementCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='elements')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} (Commande #{self.commande_id})"

    @property
    def prix_total(self):
        return self.quantite * self.prix_unitaire

class Livraison(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours de livraison'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]

    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='livraison')
    date_livraison = models.DateTimeField(default=timezone.now, verbose_name="Date de livraison prévue")
    adresse_livraison = models.CharField(max_length=255, verbose_name="Adresse de livraison")
    code_postal = models.CharField(max_length=20, blank=True, verbose_name="Code postal")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, default='Togo', verbose_name="Pays")
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name="Statut livraison")

    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-id']

    def __str__(self):
        return f'Livraison pour Commande #{self.commande.id}'

    @property
    def status_badge_class(self):
        badges = {
            'EN_ATTENTE': 'warning',
            'EN_COURS': 'primary',
            'LIVREE': 'success',
            'ANNULEE': 'danger',
        }
        return badges.get(self.statut, 'secondary')

class Notification(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(verbose_name="Message")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation', '-id']

    def __str__(self):
        return f"{self.utilisateur.nomutilisateur}: {self.message[:40]}"
