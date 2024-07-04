from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index2.html')


def index2(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

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
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès ! Vous êtes maintenant connecté.")
            return redirect('home2')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})











