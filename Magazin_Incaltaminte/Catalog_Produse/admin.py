from django.contrib import admin
from .models import Categorie, Brand, Material, Marime, Produs, StocMarime

# --- CERINȚA 7: Personalizarea paginii de administrare (titluri și header) ---
admin.site.site_header = "Administrare Magazin Încălțăminte"
admin.site.site_title = "Panou Admin Magazin"
admin.site.index_title = "Bine ai venit în panoul de control"


class CategorieAdmin(admin.ModelAdmin):
    # CERINȚA 2: Câmp de căutare după două câmpuri
    search_fields = ('nume_categorie', 'gen_tinta')

class BrandAdmin(admin.ModelAdmin):
    # CERINȚA 2: Câmp de căutare după două câmpuri
    search_fields = ('nume_brand', 'tara_origine')

class MaterialAdmin(admin.ModelAdmin):
    # CERINȚA 2: Câmp de căutare după două câmpuri
    search_fields = ('nume_material', 'instructiuni_spalare')

class MarimeAdmin(admin.ModelAdmin):
    # CERINȚA 2: Câmp de căutare după două câmpuri
    search_fields = ('valoare', 'tip_marime')


class ProdusAdmin(admin.ModelAdmin):
    # CERINȚA 1: Schimbarea ordinii implicite a afișării coloanelor
    list_display = ('nume', 'brand', 'categorie', 'pret', 'in_stoc')
    
    # CERINȚA 2: Câmp de căutare după două câmpuri
    search_fields = ('nume', 'descriere')
    
    # CERINȚA 3: Afișare în ordine descrescătoare a unei coloane (după preț: cel mai scump primul)
    ordering = ('-pret',)
    
    # CERINȚA 4: Filtre laterale pentru minim un model
    list_filter = ('categorie', 'brand', 'in_stoc')
    
    # CERINȚA 5: Schimbarea numărului de itemuri afișate la 5 (deoarece aici avem 10 produse)
    list_per_page = 5
    
    # CERINȚA 6: Împărțirea în secțiuni, din care una colapsabilă (doar cu câmpuri non-obligatorii)
    # În models.py, 'greutate' și 'material' au blank=True, null=True, deci nu sunt obligatorii!
    fieldsets = (
        ('Informații de bază', {
            'fields': ('nume', 'pret', 'descriere', 'culoare_principala', 'in_stoc')
        }),
        ('Relații / Categorisire', {
            'fields': ('categorie', 'brand')
        }),
        ('Detalii Tehnice Opționale', {
            'classes': ('collapse',), # Aceasta o face colapsabilă
            'fields': ('greutate', 'material'),
            'description': 'Aceste câmpuri pot fi lăsate goale dacă informația nu este disponibilă.'
        }),
    )


class StocMarimeAdmin(admin.ModelAdmin):
    # CERINȚA 2: Căutare după două câmpuri. Deoarece aici avem Foreign Keys, 
    # folosim dublu underscore (__) pentru a căuta în tabelele legate!
    search_fields = ('produs__nume', 'marime__valoare')
    list_display = ('produs', 'marime', 'cantitate')


# --- Înregistrarea modelelor legate de clasele lor de administrare ---
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Marime, MarimeAdmin)
admin.site.register(Produs, ProdusAdmin)
admin.site.register(StocMarime, StocMarimeAdmin)