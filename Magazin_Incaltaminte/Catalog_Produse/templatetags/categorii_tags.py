from django import template
from Catalog_Produse.models import Categorie

register = template.Library()

@register.simple_tag
def get_toate_categoriile():
    """Returnează toate categoriile din baza de date."""
    return Categorie.objects.all()