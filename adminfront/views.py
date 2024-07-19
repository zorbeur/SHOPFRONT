from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import AdministrateurCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


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
            return redirect(reverse('admin_acceuil'))
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
    return redirect(reverse('Admin_home'))






# GESTION DES PRODUITS ET DES CATEGORIES

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategorieForm, ProduitForm
from .models import Categorie, Produit

def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'categorie/liste_categorie.html', {'categories': categories})



def detail_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    return render(request, 'categorie/detail_categorie.html', {'categorie': categorie})

def creer_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'categorie/formulaire_categorie.html', {'form': form})

def modifier_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('detail_categorie', slug=categorie.slug)
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'categorie/formulaire_categorie.html', {'form': form})

def supprimer_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')
    return render(request, 'categorie/confirmation_suppression_categorie.html', {'categorie': categorie})

# Vues pour les produits
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste_produits.html', {'produits': produits})

def detail_produit(request, slug):
    produit = get_object_or_404(Produit, slug=slug)
    return render(request, 'produit/detail_produit.html', {'produit': produit})

def creer_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'produit/formulaire_produit.html', {'form': form})

def modifier_produit(request, slug):
    produit = get_object_or_404(Produit, slug=slug)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('detail_produit', slug=produit.slug)
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produit/formulaire_produit.html', {'form': form})

def supprimer_produit(request, slug):
    produit = get_object_or_404(Produit, slug=slug)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produit/confirmation_suppression_produit.html', {'produit': produit})



