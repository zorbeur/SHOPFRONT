from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import AdministrateurCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def test(request):
    return render(request, 'test.html')

def Admin_home(request):
    return render(request, 'admin_acceuil.html')

@login_required
def admin_index(request):
    return render(request, 'admin_index.html')

#inscription des admins:
@login_required
def inscription_admin(request):
    if request.method == 'POST':
        form = AdministrateurCreationForm(request.POST, request.FILES)
        if form.is_valid():
            administrateur = form.save()
            login(request, administrateur)
            return redirect(reverse('home_admin'))
    else:
        form = AdministrateurCreationForm()
    
    return render(request, 'inscription.html', {'form': form})

#connexion des admins
def connexion_admin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nomutilisateur = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            administrateur = authenticate(username=nomutilisateur, password=password)
            if administrateur is not None:
                login(request, administrateur)
                return redirect(reverse('admin_index'))
    else:
        form = AuthenticationForm()
    
    return render(request, 'connexion.html', {'form': form})

#deconnexion des admins
@login_required
def deconnexion_admin(request):
    logout(request)
    return redirect(reverse('home_admin'))






# GESTION DES PRODUITS ET DES CATEGORIES

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Categorie, Produit
from .forms import CategorieForm, ProduitForm

# Vues pour les catégories

class CategorieListView(ListView):
    model = Categorie
    template_name = 'categorie_list.html'
    context_object_name = 'categories'

class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categorie_form.html'
    success_url = reverse_lazy('categorie_list')

class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categorie_form.html'
    success_url = reverse_lazy('categorie_list')

class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = 'categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')

# Vues pour les produits

class ProduitListView(ListView):
    model = Produit
    template_name = 'produit_list.html'
    context_object_name = 'produits'

class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')

from django.shortcuts import render
from .models import Commande

def commandes_admin(request):
    commandes = Commande.objects.all()
    return render(request, 'commande_liste.html', {'commandes': commandes})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande
from .forms import CommandeForm

def mettre_a_jour_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == "POST":
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('commandes_admin')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commande_update.html', {'form': form, 'commande': commande})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande

def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == "POST":
        commande.delete()
        return redirect('commandes_admin')
    return render(request, 'supprimer_commande.html', {'commande': commande})


from django.core.mail import send_mail
from django.conf import settings

def notify_admin_of_new_order(order):
    subject = f'Nouvelle commande #{order.id}'
    message = (
        f'Une nouvelle commande a été créée.\n\n'
        f'Détails de la commande:\n'
        f'ID: {order.id}\n'
        f'Utilisateur: {order.utilisateur.nomutilisateur}\n'
        f'Total: {order.total}\n'
        f'Adresse de livraison: {order.adresse_livraison}, {order.ville}, {order.pays}\n'
        f'Statut: {order.get_etat_commande_display()}'
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['amostona82@gmail.com']

    send_mail(subject, message, from_email, recipient_list)
