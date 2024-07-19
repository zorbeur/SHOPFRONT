from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from adminfront.models import Categorie, Produit




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
    return render(request, 'cart.html')

def profil(request):
    return render(request, 'profil.html')



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
            print("Your registration is passed successfully!!!")
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès ! Vous êtes maintenant connecté.")
            return redirect('home2')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})



#ajout des vues de gestion du panier

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from adminfront.models import Panier

@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier_item, created = Panier.objects.get_or_create(utilisateur=request.user, produit=produit, commande=False)

    if not created:
        panier_item.quantite += 1
        panier_item.save()

    messages.success(request, f'{produit.nom} a été ajouté à votre panier.')
    return redirect('cart')

@login_required
def afficher_panier(request):
    panier_items = Panier.objects.filter(utilisateur=request.user, commande=False)
    total = Panier.get_total_prix_panier(request.user)
    return render(request, 'cart.html', {'panier_items': panier_items, 'total': total})

@login_required
def supprimer_du_panier(request, produit_id):
    panier_item = get_object_or_404(Panier, utilisateur=request.user, produit_id=produit_id, commande=False)
    panier_item.delete()
    messages.success(request, 'L\'article a été retiré de votre panier.')
    return redirect('panier')

def modifier_quantite(request):
    return render(request, 'index.html')







