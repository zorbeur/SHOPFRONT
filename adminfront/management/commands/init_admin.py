from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Initialise ou met à jour le compte administrateur principal par défaut pour le déploiement.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = getattr(settings, 'DEFAULT_ADMIN_USERNAME', 'admin')
        email = getattr(settings, 'DEFAULT_ADMIN_EMAIL', 'admin@eshop.tg')
        password = getattr(settings, 'DEFAULT_ADMIN_PASSWORD', 'AdminEshop2026!')

        user, created = User.objects.get_or_create(
            nomutilisateur=username,
            defaults={
                'email': email,
                'nom': 'Administrateur',
                'prenom': 'Principal',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'email_verifie': True,
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Compte administrateur par défaut créé : @{username} ({email})"))
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.email_verifie = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Compte administrateur @{username} vérifié et opérationnel."))
