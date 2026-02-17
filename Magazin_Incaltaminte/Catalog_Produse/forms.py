from django import forms
from .models import Categorie, Brand, Material

class FiltruProduseForm(forms.Form):
    # Câmpuri text
    nume = forms.CharField(max_length=150, required=False, label="Nume Produs")
    descriere = forms.CharField(max_length=200, required=False, label="Cuvânt în descriere")
    culoare_principala = forms.CharField(max_length=50, required=False, label="Culoare")
    
    # Câmpuri numerice cu MIN și MAX (Cerința ta)
    pret_min = forms.DecimalField(min_value=0, required=False, label="Preț Minim (RON)")
    pret_max = forms.DecimalField(min_value=0, required=False, label="Preț Maxim (RON)")
    
    greutate_min = forms.FloatField(min_value=0, required=False, label="Greutate Min. (g)")
    greutate_max = forms.FloatField(min_value=0, required=False, label="Greutate Max. (g)")
    
    # Câmp Boolean (Alegere cu 3 opțiuni)
    STOC_CHOICES = [('', 'Toate'), ('1', 'Doar în stoc'), ('0', 'Epuizat')]
    in_stoc = forms.ChoiceField(choices=STOC_CHOICES, required=False, label="Disponibilitate")
    
    # Câmpuri de tip Foreign Key (Relații)
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), required=False, empty_label="Toate Categoriile")
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, empty_label="Toate Brandurile")
    material = forms.ModelChoiceField(queryset=Material.objects.all(), required=False, empty_label="Toate Materialele") 