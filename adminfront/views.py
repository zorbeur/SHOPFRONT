from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import AdministrateurCreationForm, CategorieForm, ProduitForm, CommandeForm, LivraisonForm, NotificationForm
from .graphs import generate_pie_chart, generate_bar_chart, generate_status_chart
from .models import Produit, Categorie, Commande, ElementCommande, Administrateur, Livraison, Notification

def staff_required(view_func):
    """Décorateur pour s'assurer que l'utilisateur est authentifié et membre du personnel/admin."""
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='connexion_admin'
    )(view_func)
    return decorated_view

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('connexion_admin')

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

# ----------------- ACCUEIL & TABLEAU DE BORD -----------------

def Admin_home(request):
    """Portail d'entrée Admin : redirige vers le dashboard si connecté, sinon vers le login."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_index')
    return redirect('connexion_admin')

@staff_required
def admin_index(request):
    """Tableau de bord d'analyse administratif complet avec graphiques et KPIs."""
    total_produits = Produit.objects.count()
    total_categories = Categorie.objects.count()
    total_commandes = Commande.objects.count()
    total_utilisateurs = Administrateur.objects.count()

    total_ventes = Commande.objects.aggregate(total=Sum('total'))['total'] or 0

    # Produits en stock faible (<= 5)
    produits_stock_faible = Produit.objects.filter(quantite__lte=5).order_by('quantite')[:6]

    # Données graphiques
    pie_chart = generate_pie_chart()
    bar_chart = generate_bar_chart()
    status_chart = generate_status_chart()

    # Commandes récentes
    commandes_recents = Commande.objects.select_related('utilisateur').order_by('-date_commande')[:6]

    # Notifications non lues pour cet admin
    notifications_non_lues = Notification.objects.filter(utilisateur=request.user, lu=False).count()

    context = {
        'total_produits': total_produits,
        'total_categories': total_categories,
        'total_commandes': total_commandes,
        'total_utilisateurs': total_utilisateurs,
        'total_ventes': total_ventes,
        'produits_stock_faible': produits_stock_faible,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'status_chart': status_chart,
        'commandes_recents': commandes_recents,
        'notifications_non_lues': notifications_non_lues,
    }
    return render(request, 'admin_index.html', context)

# ----------------- AUTHENTIFICATION ADMIN -----------------

def connexion_admin(request):
    """Connexion pour le panneau d'administration."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nomutilisateur = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=nomutilisateur, password=password)
            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    messages.success(request, f"Bienvenue dans l'espace d'administration, {user.get_full_name()} !")
                    return redirect('admin_index')
                else:
                    messages.error(request, "Accès refusé. Vous n'avez pas les droits d'administration.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos identifiants.")
    else:
        form = AuthenticationForm()

    return render(request, 'connexion.html', {'form': form})

@login_required
def deconnexion_admin(request):
    """Déconnexion de l'administrateur."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté de l'espace administration.")
    return redirect('connexion_admin')

@staff_required
def inscription_admin(request):
    """Création d'un nouvel utilisateur ou administrateur par un admin connecté."""
    if request.method == 'POST':
        form = AdministrateurCreationForm(request.POST, request.FILES)
        if form.is_valid():
            nouvel_admin = form.save()
            messages.success(request, f"Le compte « {nouvel_admin.nomutilisateur} » a été créé avec succès.")
            return redirect('liste_clients')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AdministrateurCreationForm()

    return render(request, 'inscription.html', {'form': form})

# ----------------- GESTION DES CATÉGORIES -----------------

class CategorieListView(StaffRequiredMixin, ListView):
    model = Categorie
    template_name = 'categorie_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        qs = Categorie.objects.annotate(produits_count=Count('produit')).order_by('nom')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(nom__icontains=q)
        return qs

class CategorieCreateView(StaffRequiredMixin, CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categorie_form.html'
    success_url = reverse_lazy('categorie_list')

    def form_valid(self, form):
        messages.success(self.request, f"Catégorie « {form.instance.nom} » créée avec succès.")
        return super().form_valid(form)

class CategorieUpdateView(StaffRequiredMixin, UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categorie_form.html'
    success_url = reverse_lazy('categorie_list')

    def form_valid(self, form):
        messages.success(self.request, f"Catégorie « {form.instance.nom} » mise à jour avec succès.")
        return super().form_valid(form)

class CategorieDeleteView(StaffRequiredMixin, DeleteView):
    model = Categorie
    template_name = 'categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')

    def delete(self, request, *args, **kwargs):
        messages.info(request, "Catégorie supprimée avec succès.")
        return super().delete(request, *args, **kwargs)

# ----------------- GESTION DES PRODUITS -----------------

class ProduitListView(StaffRequiredMixin, ListView):
    model = Produit
    template_name = 'produit_list.html'
    context_object_name = 'produits'
    paginate_by = 15

    def get_queryset(self):
        qs = Produit.objects.select_related('categorie').order_by('-id')
        q = self.request.GET.get('q', '').strip()
        cat_id = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(nom__icontains=q) | Q(description__icontains=q))
        if cat_id:
            qs = qs.filter(categorie_id=cat_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProduitCreateView(StaffRequiredMixin, CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

    def form_valid(self, form):
        messages.success(self.request, f"Produit « {form.instance.nom} » ajouté avec succès.")
        return super().form_valid(form)

class ProduitUpdateView(StaffRequiredMixin, UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

    def form_valid(self, form):
        messages.success(self.request, f"Produit « {form.instance.nom} » mis à jour avec succès.")
        return super().form_valid(form)

class ProduitDeleteView(StaffRequiredMixin, DeleteView):
    model = Produit
    template_name = 'produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')

    def delete(self, request, *args, **kwargs):
        messages.info(request, "Produit supprimé avec succès.")
        return super().delete(request, *args, **kwargs)

# ----------------- GESTION DES COMMANDES -----------------

@staff_required
def commandes_admin(request):
    """Liste et filtrage des commandes pour l'administrateur."""
    commandes = Commande.objects.select_related('utilisateur').prefetch_related('elements__produit').order_by('-date_commande')

    q = request.GET.get('q', '').strip()
    if q:
        commandes = commandes.filter(
            Q(id__icontains=q) |
            Q(utilisateur__nomutilisateur__icontains=q) |
            Q(utilisateur__nom__icontains=q) |
            Q(utilisateur__prenom__icontains=q) |
            Q(ville__icontains=q)
        )

    statut = request.GET.get('statut', '').strip()
    if statut:
        commandes = commandes.filter(etat_commande=statut)

    paginator = Paginator(commandes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'commandes': page_obj,
        'page_obj': page_obj,
        'statut_choices': Commande.ETAT_CHOICES,
        'selected_statut': statut,
        'search_query': q,
        'total_count': paginator.count,
    }
    return render(request, 'commande_liste.html', context)

@staff_required
def mettre_a_jour_commande(request, commande_id):
    """Modification d'une commande existante."""
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == "POST":
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, f"Commande #{commande.id} mise à jour avec succès.")
            return redirect('commandes_admin')
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = CommandeForm(instance=commande)

    return render(request, 'commande_update.html', {'form': form, 'commande': commande})

@staff_required
def supprimer_commande(request, commande_id):
    """Suppression sécurisée d'une commande."""
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == "POST":
        commande_num = commande.id
        commande.delete()
        messages.success(request, f"Commande #{commande_num} supprimée.")
        return redirect('commandes_admin')
    return render(request, 'supprimer_commande.html', {'commande': commande})

# ----------------- GESTION DES LIVRAISONS -----------------

@staff_required
def liste_livraisons(request):
    """Liste de toutes les livraisons avec leur statut."""
    livraisons = Livraison.objects.select_related('commande__utilisateur').order_by('-id')

    statut = request.GET.get('statut', '').strip()
    if statut:
        livraisons = livraisons.filter(statut=statut)

    context = {
        'livraisons': livraisons,
        'statut_choices': Livraison.STATUT_CHOICES,
        'selected_statut': statut,
    }
    return render(request, 'livraison_liste.html', context)

@staff_required
def afficher_livraison(request, commande_id):
    """Affiche les détails de livraison pour une commande spécifique."""
    commande = get_object_or_404(Commande, id=commande_id)
    livraison, created = Livraison.objects.get_or_create(
        commande=commande,
        defaults={
            'adresse_livraison': commande.adresse_livraison,
            'ville': commande.ville,
            'code_postal': commande.code_postal,
            'pays': commande.pays,
            'statut': 'EN_ATTENTE'
        }
    )
    return render(request, 'afficher_livraison.html', {'livraison': livraison, 'commande': commande})

@staff_required
def ajouter_modifier_livraison(request, commande_id):
    """Ajouter ou modifier une livraison."""
    commande = get_object_or_404(Commande, id=commande_id)
    livraison, created = Livraison.objects.get_or_create(
        commande=commande,
        defaults={
            'adresse_livraison': commande.adresse_livraison,
            'ville': commande.ville,
            'code_postal': commande.code_postal,
            'pays': commande.pays,
            'statut': 'EN_ATTENTE'
        }
    )

    if request.method == 'POST':
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            messages.success(request, f"Livraison pour la commande #{commande.id} mise à jour.")
            return redirect('afficher_livraison', commande_id=commande.id)
    else:
        form = LivraisonForm(instance=livraison)

    return render(request, 'ajouter_modifier_livraison.html', {'form': form, 'commande': commande, 'livraison': livraison})

# ----------------- GESTION DES CLIENTS / UTILISATEURS -----------------

@staff_required
def liste_clients(request):
    """Liste de tous les clients et administrateurs avec filtres."""
    clients = Administrateur.objects.annotate(nb_commandes=Count('commandes')).order_by('-id')

    q = request.GET.get('q', '').strip()
    if q:
        clients = clients.filter(
            Q(nomutilisateur__icontains=q) |
            Q(nom__icontains=q) |
            Q(prenom__icontains=q) |
            Q(email__icontains=q)
        )

    context = {
        'clients': clients,
        'search_query': q,
        'total_clients': clients.count(),
    }
    return render(request, 'client_list.html', context)

# ----------------- NOTIFICATIONS -----------------

@staff_required
def afficher_notifications(request):
    """Affiche les notifications de l'administrateur connecté."""
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    return render(request, 'afficher_notifications.html', {'notifications': notifications})

@staff_required
def creer_notification(request):
    """Création d'une notification pour un utilisateur."""
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notif = form.save()
            messages.success(request, f"Notification envoyée à {notif.utilisateur.nomutilisateur}.")
            return redirect('afficher_notifications')
    else:
        form = NotificationForm()
    return render(request, 'creer_notification.html', {'form': form})

@staff_required
def marquer_comme_lu(request, notification_id):
    """Marque une notification comme lue."""
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    notification.lu = True
    notification.save()
    messages.success(request, "Notification marquée comme lue.")
    return redirect('afficher_notifications')

@staff_required
def supprimer_notification(request, notification_id):
    """Supprime une notification."""
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    if request.method == 'POST':
        notification.delete()
        messages.info(request, "Notification supprimée.")
        return redirect('afficher_notifications')
    return render(request, 'supprimer_notification.html', {'notification': notification})

# ----------------- VUES D'ERREUR -----------------

def custom_error_view(request, exception=None):
    """Page d'erreur 400/403/404/500 soignée."""
    return render(request, '400.html', status=400)
