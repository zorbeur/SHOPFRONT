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
    help = 'Peuple la base de données avec des données complètes et autonomes simulant 12 ans d activité (2014-2026).'

    def handle(self, *args, **options):
        import os, shutil
        self.stdout.write("Génération de l historique complet sur 12 ans (2014 - 2026)...")

        # Synchronisation automatique des images statiques vers media/
        static_img_dir = os.path.join('static', 'images')
        media_prod_dir = os.path.join('media', 'produits')
        media_cat_dir = os.path.join('media', 'categories')
        os.makedirs(media_prod_dir, exist_ok=True)
        os.makedirs(media_cat_dir, exist_ok=True)

        if os.path.exists(static_img_dir):
            for fname in os.listdir(static_img_dir):
                src = os.path.join(static_img_dir, fname)
                if os.path.isfile(src):
                    dst_prod = os.path.join(media_prod_dir, fname)
                    dst_cat = os.path.join(media_cat_dir, fname)
                    if not os.path.exists(dst_prod):
                        shutil.copy2(src, dst_prod)
                    if not os.path.exists(dst_cat):
                        shutil.copy2(src, dst_cat)

        # 1. Catégories Complètes
        categories_data = [
            ("Salon & Séjour", "Canapés grand confort, fauteuils scandinaves, tables basses en verre et bois massif pour sublimer votre séjour."),
            ("Informatique & Bureau", "Ordinateurs portables, écrans 4K, claviers mécaniques RGB, chaises ergonomiques et bureautique moderne."),
            ("Téléphonie & Tablettes", "Smartphones dernière génération, tablettes tactiles, écouteurs sans fil et accessoires de charge rapide."),
            ("Électroménager", "Réfrigérateurs basse consommation, climatiseurs inverter, micro-ondes et robots cuiseurs multifonctions."),
            ("Gaming & Consoles", "Consoles next-gen, fauteuils gaming, volants à retour de force et casques immersifs surround 7.1."),
            ("Mobilier de Chambre", "Lits coffre, matelas orthopédiques, armoires à portes coulissantes et tables de chevet contemporaines."),
            ("Luminaire & Décoration", "Lustres suspendus, lampadaires à intensité variable, appliques murales LED et décoration d'intérieur épurée."),
            ("Audio & Sonorisation", "Enceintes Bluetooth étanches, barres de son home-cinéma et systèmes audio haute fidélité."),
        ]

        categories_map = {}
        for nom, desc in categories_data:
            cat, _ = Categorie.objects.get_or_create(
                nom=nom,
                defaults={'description': desc}
            )
            categories_map[nom] = cat

        # 2. Produits Complets
        produits_data = [
            # Salon & Séjour
            ("Canapé d'Angle Panoramique Velours", "Salon & Séjour", 385000, 8, "couch2.png", "Canapé d'angle réversible 5 places avec tissu velours résistant et pieds dorés."),
            ("Fauteuil Scandinave Bois & Tissu", "Salon & Séjour", 95000, 14, "couche4.png", "Fauteuil ergonomique en tissu respirant avec structure en chêne naturel."),
            ("Table Basse Verre Trempé & Marbre", "Salon & Séjour", 125000, 10, "product1.png", "Table basse double plateau avec surface en marbre blanc et verre trempé sécurit."),
            ("Meuble TV Flottant Bois Laqué", "Salon & Séjour", 160000, 6, "product2.png", "Meuble TV moderne avec rétroéclairage LED intégré et passe-câbles discret."),
            ("Pouf Ottomane Velours Côtelé", "Salon & Séjour", 35000, 20, "product3.png", "Pouf d'appoint multifonction avec coffre de rangement intégré."),

            # Informatique & Bureau
            ("MacBook Pro M3 Max 16 Pouces", "Informatique & Bureau", 1850000, 4, "product1.png", "Puce M3 Max surpuissante, écran Liquid Retina XDR et 36 Go de mémoire unifiée."),
            ("Dell XPS 15 InfinityEdge i7", "Informatique & Bureau", 920000, 7, "product2.png", "PC ultraportable aluminium et fibre de carbone avec écran OLED 3.5K tactile."),
            ("Moniteur Gaming 27'' Incurvé 165Hz", "Informatique & Bureau", 215000, 12, "product3.png", "Écran incurvé 1500R avec temps de réponse 1ms et compatibilité FreeSync Premium."),
            ("Clavier Mécanique Sans Fil RGB", "Informatique & Bureau", 65000, 25, "sourie.png", "Switches mécaniques silencieux, rétroéclairage personnalisable et autonomie 40h."),
            ("Souris Ergonomique Sans Fil MX Master", "Informatique & Bureau", 48000, 30, "sourie.png", "Capteur haute précision 8000 DPI sur toutes surfaces et molette magnétique MagSpeed."),
            ("Chaise de Bureau Ergonomique Pro", "Informatique & Bureau", 145000, 15, "product1.png", "Support lombaire dynamique 3D, accoudoirs réglables et dossier en maille aérée."),

            # Téléphonie & Tablettes
            ("iPhone 15 Pro Max 256 Go Titane", "Téléphonie & Tablettes", 820000, 9, "product1.png", "Design en titane aérospatial, puce A17 Pro et téléobjectif 5x ultra performant."),
            ("Samsung Galaxy S24 Ultra 512 Go", "Téléphonie & Tablettes", 790000, 11, "product2.png", "Écran Dynamic AMOLED 2X, stylet S-Pen intégré et Galaxy AI révolutionnaire."),
            ("iPad Air 11 Pouces M2 Wi-Fi", "Téléphonie & Tablettes", 450000, 14, "product3.png", "Puce Apple M2 rapide, écran Liquid Retina avec True Tone et caméra avant paysage."),
            ("Écouteurs Sans Fil Pro Réduction de Bruit", "Téléphonie & Tablettes", 110000, 35, "product1.png", "Réduction active du bruit adaptative, audio spatial et autonomie cumulée 30h."),
            ("Station de Charge Rapide 3-en-1 MagSafe", "Téléphonie & Tablettes", 32000, 40, "product2.png", "Chargeur sans fil rapide pour smartphone, montre connectée et écouteurs simultanés."),

            # Électroménager
            ("Réfrigérateur Multi-Portes NoFrost 450L", "Électroménager", 580000, 5, "product1.png", "Froid ventilé intégral, distributeur d'eau fraîche et compresseur digital inverter garanti 10 ans."),
            ("Climatiseur Inverter 1.5 CV Éco-Energy", "Électroménager", 245000, 18, "product2.png", "Refroidissement express, filtre anti-poussière et économie d'énergie jusqu'à 60%."),
            ("Machine à Laver Automatique 10 Kg", "Électroménager", 310000, 8, "product3.png", "Moteur Direct Drive ultra silencieux, programme vapeur anti-allergies et essorage 1400 tr/min."),
            ("Robot Pâtissier Multifonction Inox", "Électroménager", 115000, 16, "bowl-2.png", "Bol en acier inoxydable 5.5L avec kit pâtisserie complet et mouvement planétaire."),
            ("Four Micro-Ondes Combiné Grill 28L", "Électroménager", 75000, 22, "bowl-3.png", "Cuisson combinée micro-ondes et grill avec cavité céramique facile à nettoyer."),

            # Gaming & Consoles
            ("Console PlayStation 5 Slim Édition Standard", "Gaming & Consoles", 420000, 10, "product1.png", "SSD ultra-rapide 1 To, manette DualSense à retours haptiques et graphismes 4K 120 FPS."),
            ("Console Xbox Series X 1 To", "Gaming & Consoles", 395000, 8, "product2.png", "La console la plus puissante avec 12 téraflops, Quick Resume et rétrocompatibilité totale."),
            ("Casque Gaming Sans Fil 7.1 Surround", "Gaming & Consoles", 85000, 20, "product3.png", "Microphone antibruit détachable, coussinets à mémoire de forme et récepteur sans fil 2.4 GHz."),
            ("Chaise Gaming Baquet Ergonomique Racing", "Gaming & Consoles", 135000, 12, "product1.png", "Revêtement similicuir premium, inclinaison à 180° et coussins lombaire et cervical inclus."),

            # Mobilier de Chambre
            ("Lit Coffre Capitonnée 180x200 King Size", "Mobilier de Chambre", 340000, 6, "couch2.png", "Structure renforcée en acier, sommier relevable par vérins et tête de lit matelassée."),
            ("Matelas Orthopédique Mémoire de Forme", "Mobilier de Chambre", 185000, 15, "couche4.png", "7 zones de confort ergonomiques, traitement anti-acariens et indépendance de couchage."),
            ("Armoire Dressing 3 Portes Coulissantes Miroir", "Mobilier de Chambre", 290000, 4, "product2.png", "Penderies doubles, étagères modulables et miroirs pleine longueur avec freins amortisseurs."),
            ("Table de Chevet 2 Tiroirs Chêne & Métal", "Mobilier de Chambre", 42000, 28, "product3.png", "Design industriel soigné avec coulisses télescopiques à fermeture douce."),

            # Luminaire & Décoration
            ("Lustre Suspendu Design Métal Doré", "Luminaire & Décoration", 85000, 16, "product1.png", "Suspension moderne 6 branches avec douilles E27 et finitions brossées haut de gamme."),
            ("Lampadaire d'Angle LED avec Variateur Tactile", "Luminaire & Décoration", 55000, 24, "product2.png", "Éclairage d'ambiance indirect multicolore RGBW avec télécommande et contrôle smartphone."),
            ("Miroir Mural Rond Contour Doré 80cm", "Luminaire & Décoration", 45000, 18, "product3.png", "Verre haute définition anti-éclats avec cadre métallique brossé inoxydable."),
            ("Tableau Triptyque Toile Peinte Contemporaine", "Luminaire & Décoration", 60000, 12, "img-grid-1.jpg", "Ensemble de 3 toiles tendues sur châssis en bois massif pour salon moderne."),

            # Audio & Sonorisation
            ("Barre de Son Home-Cinéma 5.1 avec Caisson", "Audio & Sonorisation", 195000, 9, "product1.png", "Puissance 450W RMS, caisson de basses sans fil et compatibilité Dolby Audio HDMI eARC."),
            ("Enceinte Bluetooth Portable Étanche IPX7", "Audio & Sonorisation", 58000, 30, "product2.png", "Basses profondes percutantes, autonomie 20h continue et résistance totale à l'eau."),
            ("Casque Bluetooth Arceau Réduction de Bruit", "Audio & Sonorisation", 140000, 15, "product3.png", "Son haute résolution Hi-Res Audio, autonomie 40 heures et oreillettes en cuir souple.")
        ]

        for nom, cat_nom, prix, qte, img_name, desc in produits_data:
            cat = categories_map.get(cat_nom)
            if cat:
                Produit.objects.get_or_create(
                    nom=nom,
                    defaults={
                        'categorie': cat,
                        'prix': Decimal(str(prix)),
                        'quantite': qte,
                        'image': f'produits/{img_name}',
                        'description': desc,
                        'date_ajout': timezone.now() - timedelta(days=random.randint(30, 2500))
                    }
                )

        prods = list(Produit.objects.all())

        # 3. Clients & Utilisateurs (Répartition de 2014 à 2026)
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

        prenoms_list = ["Koffi", "Afi", "Kokou", "Akossiwa", "Kodjo", "Adjo", "Folly", "Komi", "Mawuli", "Essi", "Kwami", "Ayawa", "Kossi", "Dodzi", "Abla", "Yawo", "Akouvi", "Kafui", "Elom", "Sena", "Sédina", "David", "Alice", "Jean-Marc", "Priscille", "Christian", "Evelyne", "Emefa", "Edem", "Kékéli"]
        noms_list = ["Lawson", "Mensah", "Agbegnenou", "Ayité", "Koudolo", "Dosseh", "Adjavon", "Gbedemah", "Koffigoh", "Gnassingbé", "Ekoué", "Amouzou", "Togbui", "Kpadé", "Tete", "Soglo", "Atikpo", "Akakpo", "Kuevi", "Dovi"]

        for i in range(1, 45):
            prenom = random.choice(prenoms_list)
            nom = random.choice(noms_list)
            username = f"{prenom.lower()}{nom.lower()}{i}"
            email = f"{username}@gmail.com"

            year = random.randint(2014, 2026)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            hour = random.randint(8, 20)
            date_inscription = timezone.make_aware(datetime(year, month, day, hour, random.randint(0, 59)))

            if not User.objects.filter(nomutilisateur=username).exists() and not User.objects.filter(email=email).exists():
                u = User.objects.create_user(
                    nomutilisateur=username,
                    email=email,
                    password="ClientPass2026!",
                    prenom=prenom,
                    nom=nom,
                    numero_de_telephone=f"+228 {random.choice([90, 91, 92, 93, 70, 71, 98, 99])} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
                    is_active=True,
                    email_verifie=True
                )
                u.date_inscription = date_inscription
                u.save()

        users = list(User.objects.all())

        # 4. Commandes Réparties sur les 12 Années (2014-2026)
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

        self.stdout.write(self.style.SUCCESS(f"[OK] Simulation 12 ans terminee avec succes : {Commande.objects.count()} commandes."))
