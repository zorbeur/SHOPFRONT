from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_superuser(sender, **kwargs):
    """Crée automatiquement l'administrateur et initialise l'historique sur 12 ans au déploiement."""
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.core.management import call_command
    from adminfront.models import Commande, Produit

    try:
        User = get_user_model()
        username = getattr(settings, 'DEFAULT_ADMIN_USERNAME', 'admin')
        email = getattr(settings, 'DEFAULT_ADMIN_EMAIL', 'admin@eshop.tg')
        password = getattr(settings, 'DEFAULT_ADMIN_PASSWORD', 'AdminEshop2026!')

        if not User.objects.filter(is_staff=True).exists() and not User.objects.filter(nomutilisateur=username).exists() and not User.objects.filter(email=email).exists():
            User.objects.create_user(
                nomutilisateur=username,
                email=email,
                password=password,
                nom='Administrateur',
                prenom='Principal',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                email_verifie=True,
            )
            print(f"[E-SHOP] Super Administrateur par défaut créé : @{username} ({email})")

        # Auto-peuplement de l'historique sur 12 ans au déploiement si la base est neuve/vide (hors mode test)
        import sys
        if 'test' not in sys.argv:
            if Commande.objects.count() == 0 or Produit.objects.count() == 0:
                call_command('seed_data')
    except Exception as e:
        pass

class AdminfrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminfront'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)
