from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import AdministrateurCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.db.models import Count
from .models import Produit, Categorie, Commande, Administrateur, Notification
from .graphs import generate_pie_chart, generate_bar_chart

def admin_index(request):
    total_produits = Produit.objects.count()
    total_categories = Categorie.objects.count()
    total_commandes = Commande.objects.count()
    total_utilisateurs = Administrateur.objects.count()
    
    produits_par_categorie = Produit.objects.values('categorie__nom').annotate(count=Count('id'))
    
    pie_chart = generate_pie_chart()
    bar_chart = generate_bar_chart()
    
    commandes_recents = Commande.objects.all().order_by('-date_commande')[:5]
    
    notifications_non_lues = Notification.objects.filter(utilisateur=request.user, lu=False).count()
    
    return render(request, 'admin_index.html', {
        'total_produits': total_produits,
        'total_categories': total_categories,
        'total_commandes': total_commandes,
        'total_utilisateurs': total_utilisateurs,
        'produits_par_categorie': produits_par_categorie,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'commandes_recents': commandes_recents,
        'notifications_non_lues': notifications_non_lues
    })


def test(request):
    return render(request, 'test.html')

def Admin_home(request):
    return render(request, 'admin_acceuil.html')


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

    def get_queryset(self):
        return Produit.objects.all().order_by('-id')

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
    commandes = Commande.objects.all().order_by('-date_commande')
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


from django.shortcuts import render
from .models import Administrateur  # Importer le modèle approprié pour les utilisateurs

def liste_clients(request):
    clients = Administrateur.objects.all()  # Modifier en fonction du modèle approprié pour les clients
    return render(request, 'client_list.html', {'clients': clients})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Livraison, Commande
from .forms import LivraisonForm  # Assurez-vous de créer un formulaire pour la livraison

def afficher_livraison(request, commande_id):
    livraison = get_object_or_404(Livraison, commande_id=commande_id)
    return render(request, 'afficher_livraison.html', {'livraison': livraison})

def ajouter_modifier_livraison(request, commande_id=None):
    if commande_id:
        livraison = get_object_or_404(Livraison, commande_id=commande_id)
    else:
        commande = get_object_or_404(Commande, id=commande_id)
        livraison = Livraison(commande=commande)

    if request.method == 'POST':
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            return redirect('afficher_livraison', commande_id=livraison.commande.id)
    else:
        form = LivraisonForm(instance=livraison)

    return render(request, 'ajouter_modifier_livraison.html', {'form': form})






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from .forms import NotificationForm

@login_required
def afficher_notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'afficher_notifications.html', {'notifications': notifications})

@login_required
def creer_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.utilisateur = request.user
            notification.save()
            return redirect('afficher_notifications')
    else:
        form = NotificationForm()
    return render(request, 'creer_notification.html', {'form': form})

@login_required
def marquer_comme_lu(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    notification.lu = True
    notification.save()
    return redirect('afficher_notifications')

@login_required
def supprimer_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    if request.method == 'POST':
        notification.delete()
        return redirect('afficher_notifications')
    return render(request, 'supprimer_notification.html', {'notification': notification})


from django.shortcuts import render

def custom_error_view(request, exception=None):
    return render(request, '400.html', status=exception.status_code if exception else 400)
