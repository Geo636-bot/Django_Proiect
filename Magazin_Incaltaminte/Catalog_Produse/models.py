from django.db import models

class Categorie(models.Model):
    GEN_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Feminin'),
        ('U', 'Unisex'),
        ('C', 'Copii')
    ]
    id_categorie = models.AutoField(primary_key=True)
    nume_categorie = models.CharField(max_length=100)
    gen_tinta = models.CharField(max_length=2, choices=GEN_CHOICES)
    vizibil_pe_site = models.BooleanField(default=True)
    
    # --- CÂMPURILE NOI PENTRU VIZUAL ---
    culoare_cod = models.CharField(max_length=7, default='#004d99', help_text="Cod HEX (ex: #FF0000)")
    icon_fontawesome = models.CharField(max_length=50, default='fa-solid fa-shoe-prints', help_text="Clasa FontAwesome")

    def __str__(self):
        return f"{self.nume_categorie} ({self.get_gen_tinta_display()})"

class Brand(models.Model):
    id_brand = models.AutoField(primary_key=True)
    
    # 3. Câmp unic (altul decât ID-ul)
    nume_brand = models.CharField(max_length=100, unique=True)
    tara_origine = models.CharField(max_length=100)
    
    # 4. Câmp care admite valori null (și poate fi lăsat gol în formular)
    an_infiintare = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nume_brand

class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nume_material = models.CharField(max_length=100)
    este_impermeabil = models.BooleanField(default=False)
    instructiuni_spalare = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nume_material

class Marime(models.Model):
    TIP_CHOICES = [
        ('EU', 'European'),
        ('US', 'American'),
        ('UK', 'Britanic')
    ]
    id_marime = models.AutoField(primary_key=True)
    valoare = models.CharField(max_length=10) # Varchar ca să accepte "38.5"
    tip_marime = models.CharField(max_length=2, choices=TIP_CHOICES)
    pentru_copii = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.valoare} ({self.tip_marime})"

class Produs(models.Model):
    id_incaltaminte = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=150)
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    descriere = models.TextField()
    in_stoc = models.BooleanField(default=True)
    
    # 5. Câmp de tip datetime, care are implicit data adăugării
    data_adaugarii = models.DateTimeField(auto_now_add=True)
    
    greutate = models.FloatField(null=True, blank=True)
    culoare_principala = models.CharField(max_length=50)

    # Relații 1 la N (One-to-Many)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)

    # Relație Many-to-Many prin tabela asociativă (StocMarime)
    marimi = models.ManyToManyField(Marime, through='StocMarime')

    def __str__(self):
        return self.nume

class StocMarime(models.Model):
    """Tabela asociativă explicitată în diagrama ta"""
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    marime = models.ForeignKey(Marime, on_delete=models.CASCADE)
    cantitate = models.IntegerField(default=0)

    class Meta:
        # Asigură-te că nu avem rânduri duplicate pentru același produs și mărime
        unique_together = ('produs', 'marime')

    def __str__(self):
        return f"{self.produs.nume} - Mărimea {self.marime.valoare} (Stoc: {self.cantitate})"