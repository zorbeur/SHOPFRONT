import matplotlib
matplotlib.use('Agg')  # Thread-safe headless backend for web servers

import io
import base64
import matplotlib.pyplot as plt
from django.db.models import Count, Sum
from .models import Produit, Commande, Categorie

# Modern theme color palette matching Sneat admin theme
CHART_COLORS = ['#696cff', '#03c3ec', '#71dd37', '#ffab00', '#ff3e1d', '#8592a3', '#56ca00', '#16b1ff', '#8c57ff', '#ffb400']

def _create_empty_chart(message="Aucune donnée disponible"):
    """Génère un graphique placeholder élégant si les données sont vides."""
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8f9fa')
    ax.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center',
            fontsize=13, color='#8592a3', fontweight='500')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#eceef1')
    
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    return img_str

def generate_pie_chart():
    """Génère un donut chart moderne de la répartition des produits par catégorie."""
    categories = Produit.objects.values('categorie__nom').annotate(count=Count('id')).order_by('-count')
    labels = [cat['categorie__nom'] or 'Sans catégorie' for cat in categories]
    sizes = [cat['count'] for cat in categories]

    if not sizes or sum(sizes) == 0:
        return _create_empty_chart("Aucun produit enregistré")

    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=110)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(labels))]

    # Donut chart with modern hole in center
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.75,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='#ffffff', linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')

    ax.legend(wedges, labels, title="Catégories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=9, title_fontsize=10, frameon=False)
    ax.set_title("Répartition des Produits par Catégorie", fontsize=12, fontweight='bold', color='#566a7f', pad=15)
    ax.axis('equal')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    return img_str

def generate_bar_chart():
    """Génère un graphique à barres moderne de l'évolution des ventes et commandes."""
    commandes = Commande.objects.values('date_commande__date').annotate(
        total=Sum('total'),
        count=Count('id')
    ).order_by('date_commande__date')[:10]

    if not commandes:
        return _create_empty_chart("Aucune commande enregistrée")

    dates = [c['date_commande__date'].strftime('%d/%m') for c in commandes]
    totals = [float(c['total']) for c in commandes]

    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=110)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    bars = ax.bar(dates, totals, color='#696cff', width=0.55, edgecolor='none', zorder=3)

    # Styling grid & spines
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#8592a3', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#eceef1')
    ax.spines['bottom'].set_color('#eceef1')
    ax.tick_params(colors='#8592a3', labelsize=9)

    ax.set_ylabel('Montant total (FCFA)', fontsize=10, color='#566a7f', labelpad=10)
    ax.set_title('Total des Ventes par Date', fontsize=12, fontweight='bold', color='#566a7f', pad=15)

    # Bar values on top
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height):,}'.replace(',', ' '),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, color='#566a7f', fontweight='600')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    return img_str

def generate_status_chart():
    """Génère un donut chart de la répartition des commandes par statut."""
    status_counts = Commande.objects.values('etat_commande').annotate(count=Count('id'))
    if not status_counts:
        return _create_empty_chart("Aucune commande enregistrée")

    labels_map = dict(Commande.ETAT_CHOICES)
    labels = [labels_map.get(sc['etat_commande'], sc['etat_commande']) for sc in status_counts]
    counts = [sc['count'] for sc in status_counts]

    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=110)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    status_color_map = {
        'EN_ATTENTE': '#ffab00',
        'EN_TRAITEMENT': '#03c3ec',
        'EXPEDIE': '#696cff',
        'LIVRE': '#71dd37',
        'ANNULE': '#ff3e1d',
    }
    colors = [status_color_map.get(sc['etat_commande'], '#8592a3') for sc in status_counts]

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,
        autopct='%1.0f%%',
        startangle=90,
        pctdistance=0.75,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='#ffffff', linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')

    ax.legend(wedges, labels, title="Statuts", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=9, title_fontsize=10, frameon=False)
    ax.set_title("Répartition des Commandes par Statut", fontsize=12, fontweight='bold', color='#566a7f', pad=15)
    ax.axis('equal')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    return img_str
