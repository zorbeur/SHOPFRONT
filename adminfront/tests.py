from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from adminfront.models import Categorie, Produit, Commande, ElementCommande, Livraison, Notification
from adminfront.graphs import generate_pie_chart, generate_bar_chart

User = get_user_model()

class AdminfrontModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            nomutilisateur='testadmin',
            email='admin@eshop.tg',
            password='securepassword123',
            prenom='Jean',
            nom='Dupont',
            is_staff=True
        )
        self.categorie = Categorie.objects.create(
            nom='Informatique & Bureau',
            description='Accessoires et matériel informatique'
        )
        self.produit = Produit.objects.create(
            nom='Clavier Mécanique RGB',
            description='Clavier rétroéclairé ultra réactif',
            prix=45000,
            quantite=10,
            categorie=self.categorie
        )

    def test_user_properties(self):
        self.assertEqual(self.user.username, 'testadmin')
        self.assertEqual(self.user.get_full_name(), 'Jean Dupont')

    def test_categorie_slug_generation(self):
        self.assertTrue(self.categorie.slug.startswith('informatique-bureau'))
        self.assertEqual(str(self.categorie), 'Informatique & Bureau')

    def test_produit_properties(self):
        self.assertTrue(self.produit.en_stock)
        self.assertTrue(self.produit.slug.startswith('clavier-mecanique-rgb'))
        self.produit.quantite = 0
        self.assertFalse(self.produit.en_stock)

    def test_commande_and_livraison_flow(self):
        cmd = Commande.objects.create(
            utilisateur=self.user,
            adresse_livraison='Lomé, Bld du Mono',
            ville='Lomé',
            pays='Togo',
            total=45000,
            etat_commande='EN_ATTENTE'
        )
        elem = ElementCommande.objects.create(
            commande=cmd,
            produit=self.produit,
            quantite=1,
            prix_unitaire=45000
        )
        self.assertEqual(elem.prix_total, 45000)
        self.assertEqual(cmd.status_badge_class, 'warning')

        livraison = Livraison.objects.create(
            commande=cmd,
            adresse_livraison=cmd.adresse_livraison,
            ville=cmd.ville,
            pays=cmd.pays,
            statut='EN_ATTENTE'
        )
        self.assertEqual(livraison.status_badge_class, 'warning')

class AdminfrontGraphTests(TestCase):
    def setUp(self):
        cat = Categorie.objects.create(nom='Test Cat')
        Produit.objects.create(nom='Prod 1', description='desc', prix=1000, quantite=5, categorie=cat)

    def test_chart_generation(self):
        pie_b64 = generate_pie_chart()
        bar_b64 = generate_bar_chart()
        self.assertIsInstance(pie_b64, str)
        self.assertIsInstance(bar_b64, str)

class AdminfrontViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            nomutilisateur='adminboss',
            email='boss@eshop.tg',
            password='adminpassword123',
            is_staff=True
        )
        self.customer_user = User.objects.create_user(
            nomutilisateur='client1',
            email='client@eshop.tg',
            password='clientpassword123',
            is_staff=False
        )
        self.categorie = Categorie.objects.create(nom='Mobilier')
        self.produit = Produit.objects.create(
            nom='Fauteuil Confort',
            description='Super fauteuil',
            prix=75000,
            quantite=3,
            categorie=self.categorie
        )

    def test_anonymous_redirect_from_admin(self):
        response = self.client.get(reverse('admin_index'))
        self.assertEqual(response.status_code, 302)

    def test_non_staff_redirect_from_admin(self):
        self.client.login(nomutilisateur='client1', password='clientpassword123')
        response = self.client.get(reverse('admin_index'))
        self.assertEqual(response.status_code, 302)

    def test_staff_access_admin_dashboard(self):
        self.client.login(nomutilisateur='adminboss', password='adminpassword123')
        response = self.client.get(reverse('admin_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tableau de Bord')

    def test_produit_list_view(self):
        self.client.login(nomutilisateur='adminboss', password='adminpassword123')
        response = self.client.get(reverse('produit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fauteuil Confort')

    def test_categorie_list_view(self):
        self.client.login(nomutilisateur='adminboss', password='adminpassword123')
        response = self.client.get(reverse('categorie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mobilier')
