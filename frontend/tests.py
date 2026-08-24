from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from adminfront.models import Categorie, Produit, Commande, ElementCommande, Livraison

User = get_user_model()

class FrontendViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            nomutilisateur='client_tester',
            email='tester@eshop.tg',
            password='testpassword123',
            prenom='Alice',
            nom='Martin',
            numero_de_telephone='+228 90 00 00 00'
        )
        self.categorie = Categorie.objects.create(
            nom='Salon & Séjour',
            description='Canapés et tables basses'
        )
        self.produit1 = Produit.objects.create(
            nom='Canapé d Angle Velours',
            description='Canapé grand confort',
            prix=150000,
            quantite=5,
            categorie=self.categorie
        )
        self.produit2 = Produit.objects.create(
            nom='Lampe de Chevet LED',
            description='Lampe design moderne',
            prix=15000,
            quantite=20,
            categorie=self.categorie
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mobilier')
        self.assertContains(response, 'Boutique')

    def test_shop_page_and_filtering(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Canapé d Angle Velours')

        # Test Search
        response_search = self.client.get(reverse('shop') + '?q=Lampe')
        self.assertEqual(response_search.status_code, 200)
        self.assertContains(response_search, 'Lampe de Chevet LED')
        self.assertNotContains(response_search, 'Canapé d Angle Velours')

        # Test Category Filter
        response_cat = self.client.get(reverse('shop') + f'?category={self.categorie.slug}')
        self.assertEqual(response_cat.status_code, 200)
        self.assertContains(response_cat, 'Salon &amp; Séjour')

    def test_product_detail_page(self):
        response = self.client.get(reverse('produit_detail', args=[self.produit1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Canapé d Angle Velours')
        self.assertContains(response, 'FCFA')

    def test_wishlist_operations(self):
        # Toggle Wishlist AJAX
        response_add = self.client.post(
            reverse('toggle_wishlist', args=[self.produit1.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response_add.status_code, 200)
        self.assertTrue(response_add.json()['added'])

        # Check wishlist page
        response_page = self.client.get(reverse('wishlist'))
        self.assertEqual(response_page.status_code, 200)
        self.assertContains(response_page, 'Canapé d Angle Velours')

    def test_public_order_tracking(self):
        cmd = Commande.objects.create(
            utilisateur=self.user,
            adresse_livraison='Agoè, Lomé',
            ville='Lomé',
            pays='Togo',
            total=150000,
            etat_commande='EXPEDIE'
        )
        # Search by order ID
        response = self.client.get(reverse('suivi_commande_public') + f'?q={cmd.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Commande #{cmd.id}')

    def test_auxiliary_pages(self):
        for route in ['about', 'services', 'blog', 'contact', 'faq', 'conditions_livraison', 'confidentialite', 'promotions']:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)

    def test_cart_operations(self):
        # 1. Ajouter au panier via AJAX
        response = self.client.post(
            reverse('ajouter_au_panier', args=[self.produit2.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['cart_count'], 1)

        # 2. Vérifier page panier
        response_cart = self.client.get(reverse('cart'))
        self.assertEqual(response_cart.status_code, 200)
        self.assertContains(response_cart, 'Lampe de Chevet LED')
        self.assertEqual(response_cart.context['frais_livraison'], 1500)
        self.assertEqual(response_cart.context['cart_total'], 16500)

        # 3. Mettre à jour quantité
        response_update = self.client.post(
            reverse('update_cart_item', args=[self.produit2.id]),
            {'quantite': 4}
        )
        self.assertEqual(response_update.status_code, 302)
        response_cart2 = self.client.get(reverse('cart'))
        self.assertEqual(response_cart2.context['frais_livraison'], 0)
        self.assertEqual(response_cart2.context['cart_total'], 60000)

        # 4. Supprimer l'article du panier
        response_del = self.client.post(reverse('delete_cart_item', args=[self.produit2.id]))
        self.assertEqual(response_del.status_code, 302)
        response_cart3 = self.client.get(reverse('cart'))
        self.assertEqual(response_cart3.context['cart_count'], 0)

    def test_checkout_flow(self):
        # Panier avec produit 1
        self.client.post(reverse('ajouter_au_panier', args=[self.produit1.id]))

        # Sans être connecté -> redirection vers connexion
        response_checkout_anon = self.client.get(reverse('paiement'))
        self.assertEqual(response_checkout_anon.status_code, 302)

        # Connecté -> accès et validation de la commande
        self.client.login(nomutilisateur='client_tester', password='testpassword123')
        response_checkout_auth = self.client.get(reverse('paiement'))
        self.assertEqual(response_checkout_auth.status_code, 200)

        # Passer commande
        response_order = self.client.post(reverse('paiement'), {
            'adresse': 'Quartier Administratif, Rue 45',
            'ville': 'Lomé',
            'pays': 'Togo',
            'telephone': '+228 90 00 00 00',
            'methode_paiement': 'LIVRAISON',
            'notes': 'Livrer en matinée svp'
        })
        self.assertEqual(response_order.status_code, 302)
        
        cmd = Commande.objects.filter(utilisateur=self.user).last()
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd.total, 150000)
        self.assertEqual(cmd.elements.count(), 1)
        self.assertTrue(Livraison.objects.filter(commande=cmd).exists())

        response_cart_after = self.client.get(reverse('cart'))
        self.assertEqual(response_cart_after.context['cart_count'], 0)

    def test_user_authentication_and_profile(self):
        response_reg = self.client.post(reverse('enregistrement'), {
            'prenom': 'David',
            'nom': 'Lawson',
            'nomutilisateur': 'davidl',
            'email': 'david@eshop.tg',
            'numero_de_telephone': '+228 91 22 33 44',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        })
        self.assertEqual(response_reg.status_code, 302)
        self.assertTrue(User.objects.filter(nomutilisateur='davidl').exists())

        self.client.login(nomutilisateur='davidl', password='newuserpass123')
        response_prof = self.client.get(reverse('profil'))
        self.assertEqual(response_prof.status_code, 200)
        self.assertContains(response_prof, 'David Lawson')
