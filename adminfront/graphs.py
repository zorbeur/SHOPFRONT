from django.db.models import Count, Sum
from .models import Commande
import io
import base64
import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import Produit

def generate_pie_chart():
    categories = Produit.objects.values('categorie__nom').annotate(count=Count('id')).order_by('categorie__nom')
    labels = [cat['categorie__nom'] for cat in categories]
    sizes = [cat['count'] for cat in categories]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    return img_str

def generate_bar_chart():
    commandes = Commande.objects.values('date_commande').annotate(total=Sum('total')).order_by('date_commande')
    dates = [commande['date_commande'] for commande in commandes]
    totals = [commande['total'] for commande in commandes]
    
    fig, ax = plt.subplots()
    ax.bar(dates, totals)
    ax.set_xlabel('Date')
    ax.set_ylabel('Total')
    ax.set_title('Total des Commandes par Date')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    return img_str
