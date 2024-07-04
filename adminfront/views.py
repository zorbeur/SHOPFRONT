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
def inscription_admin(request):
    if request.method == 'POST':
        form = AdministrateurCreationForm(request.POST, request.FILES)
        if form.is_valid():
            administrateur = form.save()
            login(request, administrateur)
            return redirect(reverse('admin_index'))
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
def deconnexion_admin(request):
    logout(request)
    return redirect(reverse('connexion_admin'))

# Gestion des fonctionnalites de notre liste deroulante Menus

