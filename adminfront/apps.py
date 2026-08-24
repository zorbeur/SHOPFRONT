from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_superuser(sender, **kwargs):
    """Crée automatiquement un administrateur par défaut après chaque migration si aucun staff n'existe."""
    from django.conf import settings
    from django.contrib.auth import get_user_model
    try:
        User = get_user_model()
        username = getattr(settings, 'DEFAULT_ADMIN_USERNAME', 'admin')
        email = getattr(settings, 'DEFAULT_ADMIN_EMAIL', 'admin@eshop.tg')
        password = getattr(settings, 'DEFAULT_ADMIN_PASSWORD', 'AdminEshop2026!')

        if not User.objects.filter(is_staff=True).exists() and not User.objects.filter(nomutilisateur=username).exists() and not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
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
    except Exception:
        pass

class AdminfrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminfront'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)
