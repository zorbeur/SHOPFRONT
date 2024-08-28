import json
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminfront.models import Categorie, Produit ,Commande
from adminfront.models import Commande, ElementCommande, Cart , Produit






def index(request):
    Categories=Categorie.objects.all()
    return render(request, 'index2.html', {Categories:Categories} )


def index2(request):
    return render(request, 'index.html')

def shop(request):
    # Récupérer toutes les catégories avec leurs produits associés
    categories = Categorie.objects.prefetch_related('produit_set').all()
    
    context = {
        'categories': categories
    }
    return render(request, 'shop.html', context)


def about(request):
    return render(request, 'checkout.html')

def services(request):
    return render(request, 'services.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

@login_required

def cart(request):
    panier = request.session.get('panier', {})
    cart_items = []
    cart_subtotal = 0
    cart_total = 0
    
    for produit_id, item in panier.items():
        produit = Produit.objects.get(id=produit_id)
        item_total = produit.prix * item['quantite']
        cart_items.append({
            'id': produit.id,
            'nom': produit.nom,
            'prix': produit.prix,
            'quantite': item['quantite'],
            'image': produit.image,
            'total_prix': item_total,
        })
        cart_subtotal += item_total
        cart_total += item_total  # Ajouter les frais d'expédition ou les taxes si nécessaire
    
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
    }
    
    return render(request, 'cart.html', context)



@login_required
def profil(request):
    # Assurez-vous que l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige vers la page de connexion si l'utilisateur n'est pas authentifié

    commandes = Commande.objects.filter(utilisateur=request.user)
    context = {
        'user': request.user,
        'commandes': commandes,
    }
    return render(request, 'profil.html', context)


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home2')  # Redirige vers la vue 'index2' après une connexion réussie
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    
    return render(request, 'login.html')


def enregistrement(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès ! Vous êtes maintenant connecté.")
            return redirect('home2')  # Redirige vers la vue 'home2' après une connexion réussie
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})



@require_POST
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    data = json.loads(request.body)
    quantite = int(data.get('quantite', 1))

    panier = request.session.get('panier', {})
    if str(produit_id) in panier:
        panier[str(produit_id)]['quantite'] += quantite
    else:
        panier[str(produit_id)] = {'quantite': quantite, 'prix': str(produit.prix)}

    request.session['panier'] = panier
    return JsonResponse({'status': 'success'})



def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        panier = request.session.get('panier', {})
        
        if str(item_id) in panier:
            panier[str(item_id)]['quantite'] = quantite
        
        request.session['panier'] = panier
        return redirect('cart')

from django.shortcuts import redirect

def delete_cart_item(request, item_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        
        if str(item_id) in panier:
            del panier[str(item_id)]
        
        request.session['panier'] = panier
        return redirect('cart')





@login_required
@login_required  # Assurez-vous que l'utilisateur est connecté
def paiement(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('cart')  # Redirige vers la page du panier si le panier est vide

    cart_items = []
    cart_subtotal = 0
    cart_total = 0

    for produit_id, item in panier.items():
        produit = Produit.objects.get(id=produit_id)
        item_total = produit.prix * item['quantite']
        cart_items.append({
            'id': produit.id,
            'nom': produit.nom,
            'prix': produit.prix,
            'quantite': item['quantite'],
            'image': produit.image,
            'total_prix': item_total,
        })
        cart_subtotal += item_total
        cart_total += item_total  # Ajouter les frais d'expédition ou les taxes si nécessaire

    user = request.user
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
        'nom': user.get_full_name(),  # Nom complet de l'utilisateur
        'adresse': 'Lome-Togo',
        'ville': 'Kegue',
        'code_postal': '10334',
        'pays': 'Togo',
    }

    return render(request, 'paiement.html', context)


@login_required
def process_payment(request):
    if request.method == 'POST':
        utilisateur = request.user

        # Calculer le total basé sur les sessions
        panier = request.session.get('panier', {})
        total = 0
        for produit_id, item in panier.items():
            produit = Produit.objects.get(id=produit_id)
            total += produit.prix * item['quantite']

        # Créer une commande
        commande = Commande.objects.create(
            utilisateur=utilisateur,
            total=total,
            adresse_livraison=request.POST['adresse'],
            code_postal=request.POST['code_postal'],
            ville=request.POST['ville'],
            pays=request.POST['pays']
        )

        # Ajouter les articles du panier à la commande
        for produit_id, item in panier.items():
            produit = Produit.objects.get(id=produit_id)
            ElementCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=item['quantite'],
                prix_unitaire=produit.prix
            )

        # Vider le panier
        request.session['panier'] = {}

        # Envoyer un SMS de confirmation
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Votre commande #{commande.id} a été passée avec succès ! Total : {total} FCFA.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to='+22897621296'  # Remplacez par le numéro du client si nécessaire
        )

        # Afficher un message de succès
        messages.success(request, 'Votre commande a été passée avec succès !')

        # Rediriger vers la page de remerciement en passant l'ID de la commande
        return redirect('merci', commande_id=commande.id)
    else:
        return redirect('cart')



def calculate_cart_total(utilisateur):
    # Fonction pour calculer le total du panier
    cart_items = get_cart_items(utilisateur)
    total = sum(item.produit.prix * item.quantite for item in cart_items)
    return total

def get_cart_items(utilisateur):
    # Fonction pour récupérer les éléments du panier de l'utilisateur
    return utilisateur.cart.items.all()

def clear_cart(utilisateur):
    # Fonction pour vider le panier de l'utilisateur
    utilisateur.cart.items.all().delete()


def merci(request, commande_id):
    # Vous pouvez récupérer les informations de la commande si nécessaire
    return render(request, 'merci.html', {'commande_id': commande_id})


def commande_status(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_status.html', {'commande': commande})
