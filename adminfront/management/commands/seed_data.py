import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from adminfront.models import Categorie, Produit, Commande, ElementCommande, Livraison, Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données simulant 12 ans d activité (2014-2026).'

    def handle(self, *args, **options):
        self.stdout.write("Génération de l historique e-commerce sur 12 ans (2014 - 2026)...")

        prods = list(Produit.objects.all())
        users = list(User.objects.all())

        villes_togo = [
            ("Lomé (Golfe)", "Agoè-Nyivé, Rue 45"),
            ("Lomé (Maritime)", "Bè Plage, Bld du Mono"),
            ("Lomé (Tokoin)", "Tokoin Casablanca, Villa 12"),
            ("Lomé (Hedzranawoé)", "Hedzranawoé Marché, Rue des Palmiers"),
            ("Kpalimé", "Quartier Zomayi, Route de Kloto"),
            ("Kara", "Quartier Chaminade, Bld Central"),
            ("Sokodé", "Quartier Didaourè, Avenue de la Paix"),
            ("Atakpamé", "Quartier Agbonou, Rue du Commerce"),
            ("Dapaong", "Quartier Nassablé, Route Nationale 1"),
            ("Tsévié", "Quartier Davié, Bld des Martyrs"),
            ("Aného", "Quartier Nlessi, Bld de l'Océan")
        ]

        commandes_cibles = {
            2014: 8, 2015: 12, 2016: 18, 2017: 24, 2018: 32, 2019: 45,
            2020: 44, 2021: 40, 2022: 50, 2023: 60, 2024: 70, 2025: 80, 2026: 35
        }

        created = 0
        with transaction.atomic():
            for year, target_count in commandes_cibles.items():
                existing = Commande.objects.filter(date_commande__year=year).count()
                needed = max(0, target_count - existing)

                for _ in range(needed):
                    u = random.choice(users)
                    month = random.randint(1, 8 if year == 2026 else 12)
                    day = random.randint(1, 28)
                    hour = random.randint(8, 20)
                    date_cmd = timezone.make_aware(datetime(year, month, day, hour, random.randint(0, 59)))
                    etat = 'LIVRE' if year <= 2025 else random.choices(['LIVRE', 'EXPEDIE', 'EN_TRAITEMENT', 'EN_ATTENTE'], weights=[55, 25, 12, 8])[0]
                    v_info = random.choice(villes_togo)

                    cmd = Commande.objects.create(
                        utilisateur=u,
                        date_commande=date_cmd,
                        total=Decimal('0.00'),
                        adresse_livraison=v_info[1],
                        ville=v_info[0],
                        pays='Togo',
                        etat_commande=etat
                    )

                    p_sel = random.sample(prods, min(random.randint(1, 3), len(prods)))
                    tot = Decimal('0.00')
                    for p in p_sel:
                        q = random.randint(1, 2)
                        ElementCommande.objects.create(commande=cmd, produit=p, quantite=q, prix_unitaire=p.prix)
                        tot += (p.prix * q)

                    if tot < Decimal('50000.00'):
                        tot += Decimal('1500.00')
                    cmd.total = tot
                    cmd.save()

                    st = 'LIVREE' if etat == 'LIVRE' else ('EN_COURS' if etat in ('EXPEDIE', 'EN_TRAITEMENT') else 'EN_ATTENTE')
                    Livraison.objects.get_or_create(
                        commande=cmd,
                        defaults={
                            'adresse_livraison': cmd.adresse_livraison,
                            'ville': cmd.ville,
                            'pays': cmd.pays,
                            'statut': st,
                            'date_livraison': date_cmd + timedelta(days=2)
                        }
                    )
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] {created} commandes generees. Total : {Commande.objects.count()}."))
