from adminfront.models import Categorie, Produit

def cart_context(request):
    """
    Context processor providing cart items count, total, and categories across all templates.
    """
    panier = request.session.get('panier', {})
    cart_count = sum(item.get('quantite', 1) for item in panier.values())
    cart_total = 0
    for prod_id, item in panier.items():
        try:
            prod = Produit.objects.filter(id=prod_id).first()
            if prod:
                cart_total += float(prod.prix) * item.get('quantite', 1)
        except Exception:
            pass

    return {
        'cart_count': cart_count,
        'cart_total_global': cart_total,
        'global_categories': Categorie.objects.all(),
    }
