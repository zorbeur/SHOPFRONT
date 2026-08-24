import json
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from adminfront.models import Categorie, Produit, Commande, ElementCommande, Livraison, Notification
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, CheckoutForm, ContactForm

def _get_cart_data(request):
    """Calcule proprement les éléments, sous-total et total du panier de session."""
    panier = request.session.get('panier', {})
    cart_items = []
    cart_subtotal = Decimal('0.00')

    for produit_id, item in list(panier.items()):
        try:
            produit = Produit.objects.filter(id=produit_id).first()
            if not produit:
                continue
            quantite = int(item.get('quantite', 1))
            if quantite <= 0:
                continue
            item_total = produit.prix * quantite
            cart_items.append({
                'id': produit.id,
                'produit': produit,
                'nom': produit.nom,
                'prix': produit.prix,
                'quantite': quantite,
                'image': produit.image,
                'total_prix': item_total,
                'en_stock': produit.en_stock,
            })
            cart_subtotal += item_total
        except Exception:
            continue

    # Frais de livraison : gratuits à partir de 50 000 FCFA, sinon 1500 FCFA si panier non vide
    frais_livraison = Decimal('0.00')
    if cart_subtotal > Decimal('0.00') and cart_subtotal < Decimal('50000.00'):
        frais_livraison = Decimal('1500.00')

    cart_total = cart_subtotal + frais_livraison

    return {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'frais_livraison': frais_livraison,
        'cart_total': cart_total,
        'cart_count': sum(item['quantite'] for item in cart_items),
    }

def index(request):
    """Page d'accueil moderne avec catégories en vedette et produits populaires."""
    categories = Categorie.objects.all()[:6]
    produits_vedettes = Produit.objects.filter(quantite__gt=0).order_by('-id')[:8]
    nouveautes = Produit.objects.order_by('-date_ajout')[:4]

    context = {
        'categories': categories,
        'produits_vedettes': produits_vedettes,
        'nouveautes': nouveautes,
    }
    return render(request, 'index.html', context)

def index2(request):
    return redirect('home')

def shop(request):
    """Page boutique avec recherche, filtre par catégorie et tri."""
    categories = Categorie.objects.all()
    produits = Produit.objects.all()

    # Filtre par recherche textuelle
    query = request.GET.get('q', '').strip()
    if query:
        produits = produits.filter(Q(nom__icontains=query) | Q(description__icontains=query))

    # Filtre par catégorie (slug ou id)
    categorie_slug = request.GET.get('category', '').strip()
    active_category = None
    if categorie_slug:
        active_category = Categorie.objects.filter(slug=categorie_slug).first()
        if active_category:
            produits = produits.filter(categorie=active_category)

    # Tri
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        produits = produits.order_by('prix')
    elif sort == 'price_desc':
        produits = produits.order_by('-prix')
    elif sort == 'name_asc':
        produits = produits.order_by('nom')
    else:
        produits = produits.order_by('-id')

    # Pagination (12 par page)
    paginator = Paginator(produits, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'produits': page_obj,
        'page_obj': page_obj,
        'query': query,
        'active_category': active_category,
        'sort': sort,
        'total_count': paginator.count,
    }
    return render(request, 'shop.html', context)

def about(request):
    """Page À propos de l'entreprise."""
    return render(request, 'about.html')

def services(request):
    """Page Services proposés."""
    return render(request, 'services.html')

def blog(request):
    """Page Blog et actualités."""
    return render(request, 'blog.html')

def contact(request):
    """Page de contact avec formulaire fonctionnel."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Merci pour votre message ! Notre équipe vous répondra dans les plus brefs délais.")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def cart(request):
    """Affichage détaillé du panier client."""
    cart_data = _get_cart_data(request)
    return render(request, 'cart.html', cart_data)

def ajouter_au_panier(request, produit_id):
    """Ajoute un produit au panier (gère AJAX JSON et requêtes POST classiques)."""
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        quantite = 1
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                quantite = int(data.get('quantite', 1))
            except Exception:
                quantite = 1
        else:
            try:
                quantite = int(request.POST.get('quantite', 1))
            except ValueError:
                quantite = 1

        if quantite < 1:
            quantite = 1

        panier = request.session.get('panier', {})
        pid_str = str(produit_id)

        if pid_str in panier:
            panier[pid_str]['quantite'] += quantite
        else:
            panier[pid_str] = {'quantite': quantite, 'prix': str(produit.prix)}

        request.session['panier'] = panier
        request.session.modified = True

        total_items = sum(item['quantite'] for item in panier.values())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'success': True,
                'message': f"« {produit.nom} » a été ajouté à votre panier.",
                'cart_count': total_items,
            })

        messages.success(request, f"« {produit.nom} » a été ajouté à votre panier.")
        return redirect(request.META.get('HTTP_REFERER', 'shop'))

    return redirect('shop')

def update_cart_item(request, item_id):
    """Met à jour la quantité d'un article du panier."""
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        pid_str = str(item_id)

        try:
            quantite = int(request.POST.get('quantite', 1))
        except ValueError:
            quantite = 1

        if pid_str in panier:
            if quantite > 0:
                panier[pid_str]['quantite'] = quantite
            else:
                del panier[pid_str]

            request.session['panier'] = panier
            request.session.modified = True
            messages.success(request, "Panier mis à jour.")

    return redirect('cart')

def delete_cart_item(request, item_id):
    """Supprime un article du panier."""
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        pid_str = str(item_id)

        if pid_str in panier:
            del panier[pid_str]
            request.session['panier'] = panier
            request.session.modified = True
            messages.info(request, "Article retiré du panier.")

    return redirect('cart')

@login_required
def paiement(request):
    """Page de commande et paiement avec formulaire de livraison."""
    cart_data = _get_cart_data(request)
    if not cart_data['cart_items']:
        messages.warning(request, "Votre panier est vide. Ajoutez des produits avant de passer commande.")
        return redirect('shop')

    user = request.user
    initial_data = {
        'adresse': '',
        'ville': 'Lomé',
        'code_postal': '00228',
        'pays': 'Togo',
        'telephone': getattr(user, 'numero_de_telephone', ''),
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            adresse = form.cleaned_data['adresse']
            ville = form.cleaned_data['ville']
            code_postal = form.cleaned_data.get('code_postal', '')
            pays = form.cleaned_data['pays']
            methode = form.cleaned_data['methode_paiement']

            # Création de la commande
            commande = Commande.objects.create(
                utilisateur=user,
                total=cart_data['cart_total'],
                adresse_livraison=adresse,
                code_postal=code_postal,
                ville=ville,
                pays=pays,
                etat_commande='EN_ATTENTE'
            )

            # Création des éléments de la commande
            for item in cart_data['cart_items']:
                ElementCommande.objects.create(
                    commande=commande,
                    produit=item['produit'],
                    quantite=item['quantite'],
                    prix_unitaire=item['prix']
                )
                # Décrémentation du stock
                prod = item['produit']
                prod.quantite = max(0, prod.quantite - item['quantite'])
                prod.save(update_fields=['quantite'])

            # Création de la livraison associée
            Livraison.objects.create(
                commande=commande,
                adresse_livraison=adresse,
                code_postal=code_postal,
                ville=ville,
                pays=pays,
                statut='EN_ATTENTE'
            )

            # Notification interne pour l'administrateur
            Notification.objects.create(
                utilisateur=user,
                message=f"Nouvelle commande #{commande.id} passée par {user.get_full_name()} ({commande.total} FCFA)."
            )

            # Tentative SMS Twilio (optionnelle et sécurisée)
            if getattr(settings, 'TWILIO_ACCOUNT_SID', '') and getattr(settings, 'TWILIO_AUTH_TOKEN', ''):
                try:
                    from twilio.rest import Client as TwilioClient
                    tclient = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    client_phone = form.cleaned_data.get('telephone') or getattr(user, 'numero_de_telephone', '')
                    if client_phone:
                        tclient.messages.create(
                            body=f"ESHOP : Votre commande #{commande.id} d'un montant de {commande.total} FCFA a été enregistrée avec succès !",
                            from_=settings.TWILIO_PHONE_NUMBER,
                            to=client_phone
                        )
                except Exception as e:
                    print(f"Twilio SMS notice: {e}")

            # Vider le panier de session
            request.session['panier'] = {}
            request.session.modified = True

            messages.success(request, f"Votre commande #{commande.id} a été confirmée avec succès !")
            return redirect('merci', commande_id=commande.id)
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        **cart_data,
        'form': form,
    }
    return render(request, 'paiement.html', context)

def process_payment(request):
    """Redirection de secours vers paiement."""
    return redirect('paiement')

def merci(request, commande_id):
    """Page de confirmation et remerciement après commande."""
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'merci.html', {'commande': commande, 'commande_id': commande.id})

def commande_status(request, commande_id):
    """Suivi interactif de l'état de la commande."""
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_status.html', {'commande': commande})

@login_required
def profil(request):
    """Tableau de bord utilisateur avec gestion du profil et historique des commandes."""
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profil')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserProfileForm(instance=user)

    commandes = Commande.objects.filter(utilisateur=user).prefetch_related('elements__produit').order_by('-date_commande')
    total_depense = sum(c.total for c in commandes)

    context = {
        'user': user,
        'form': form,
        'commandes': commandes,
        'total_depense': total_depense,
    }
    return render(request, 'profil.html', context)

def connexion(request):
    """Connexion client propre."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Heureux de vous revoir, {user.get_full_name()} !")
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def enregistrement(request):
    """Inscription client avec le modèle Administrateur / Utilisateur."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Félicitations, votre compte a été créé avec succès ! Bienvenue sur E-SHOP.")
            return redirect('home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})

def deconnexion(request):
    """Déconnexion sécurisée."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

# ----------------- NOUVELLES PAGES COMPLÉMENTAIRES -----------------

def produit_detail(request, pk=None, slug=None):
    """Page détaillée d'un produit avec galerie, caractéristiques et articles similaires."""
    if slug:
        produit = get_object_or_404(Produit, slug=slug)
    else:
        produit = get_object_or_404(Produit, pk=pk)

    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:4]

    wishlist = request.session.get('wishlist', [])
    is_in_wishlist = produit.id in wishlist

    context = {
        'produit': produit,
        'produits_similaires': produits_similaires,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'produit_detail.html', context)

def suivi_commande_public(request):
    """Page publique de recherche et de suivi d'un colis par numéro de commande ou téléphone."""
    commande = None
    recherche_effectuee = False
    query = request.GET.get('q', '').strip()

    if query:
        recherche_effectuee = True
        # Chercher par ID numérique ou par numéro de téléphone du client
        if query.startswith('#'):
            clean_query = query[1:]
        else:
            clean_query = query

        if clean_query.isdigit():
            commande = Commande.objects.filter(id=int(clean_query)).prefetch_related('elements__produit').first()

        if not commande:
            commande = Commande.objects.filter(
                Q(utilisateur__numero_de_telephone__icontains=query) |
                Q(adresse_livraison__icontains=query)
            ).order_by('-date_commande').first()

    return render(request, 'suivi_commande.html', {
        'commande': commande,
        'query': query,
        'recherche_effectuee': recherche_effectuee,
    })

def wishlist(request):
    """Page Liste d'Envies (Favoris) stockée en session."""
    wishlist_ids = request.session.get('wishlist', [])
    produits = Produit.objects.filter(id__in=wishlist_ids)
    return render(request, 'wishlist.html', {'produits': produits})

def toggle_wishlist(request, produit_id):
    """Ajoute ou retire un produit des favoris (gère AJAX et redirection)."""
    produit = get_object_or_404(Produit, id=produit_id)
    wishlist = request.session.get('wishlist', [])

    if produit_id in wishlist:
        wishlist.remove(produit_id)
        added = False
        msg = f"« {produit.nom} » a été retiré de vos favoris."
    else:
        wishlist.append(produit_id)
        added = True
        msg = f"« {produit.nom} » a été ajouté à vos favoris !"

    request.session['wishlist'] = wishlist
    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'added': added,
            'message': msg,
            'wishlist_count': len(wishlist),
        })

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

def faq(request):
    """Page Foire Aux Questions (FAQ) détaillée."""
    return render(request, 'faq.html')

def conditions_livraison(request):
    """Page Conditions Générales de Vente, Livraison et Retours."""
    return render(request, 'conditions_livraison.html')

def confidentialite(request):
    """Page Politique de Confidentialité et Protection des Données."""
    return render(request, 'confidentialite.html')

def promotions(request):
    """Page dédiée aux Promotions, Soldes et Bons Plans."""
    produits_promo = Produit.objects.filter(quantite__gt=0).order_by('-date_ajout')
    return render(request, 'promotions.html', {'produits': produits_promo})
