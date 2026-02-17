from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Categorie, Brand, Material,Produs,CustomUser
import re

class FiltruProduseForm(forms.Form):
    # 1. Widget-uri specifice pentru text (TextInput)
    nume = forms.CharField(
        max_length=150, required=False, label="Nume Produs",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Air Max'})
    )
    descriere = forms.CharField(
        max_length=200, required=False, label="Cuvânt în descriere",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: confortabil'})
    )
    culoare_principala = forms.CharField(
        max_length=50, required=False, label="Culoare",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Alb'})
    )
    
    # 2. Widget-uri specifice pentru numere (NumberInput)
    pret_min = forms.DecimalField(
        min_value=0, required=False, label="Preț Minim (RON)",
        initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0.00'})
    )
    pret_max = forms.DecimalField(
        min_value=0, required=False, label="Preț Maxim (RON)",
        widget=forms.NumberInput(attrs={'placeholder': '1000.00'})
    )
    
    greutate_min = forms.FloatField(
        min_value=0, required=False, label="Greutate Min. (g)",
        initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '100'})
    )
    greutate_max = forms.FloatField(
        min_value=0, required=False, label="Greutate Max. (g)",
        widget=forms.NumberInput(attrs={'placeholder': '500'})
    )

    # 3. Widget specific pentru dată (DateInput) - Adăugat pentru a respecta cerința!
    data_adaugarii_min = forms.DateField(
        required=False, label="Adăugat după data:",
        # Îi specificăm HTML-ului că este de tip 'date' pentru a afișa calendarul!
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )
    
    # 4. Widget-uri specifice pentru Dropdown/Select (Select)
    STOC_CHOICES = [('', 'Toate'), ('1', 'Doar în stoc'), ('0', 'Epuizat')]
    in_stoc = forms.ChoiceField(
        choices=STOC_CHOICES, required=False, label="Disponibilitate",
        widget=forms.Select()
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(), required=False, empty_label="Toate Categoriile",
        widget=forms.Select()
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(), required=False, empty_label="Toate Brandurile",
        widget=forms.Select()
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), required=False, empty_label="Toate Materialele",
        widget=forms.Select()
    )
    PAGINARE_CHOICES = [('5', '5 pe pagină'), ('10', '10 pe pagină'), ('20', '20 pe pagină'), ('100', '100 pe pagină')]
    items_pe_pagina = forms.ChoiceField(
        choices=PAGINARE_CHOICES, 
        required=False, 
        label="Produse pe pagină",
        initial='5',
        widget=forms.Select()
    )

    # --- CELE 3 VALIDĂRI PERSONALIZATE ---

    # Validarea 1: Verificăm un singur câmp (Numele) folosind metoda clean_<nume_camp>
    def clean_nume(self):
        nume_introdus = self.cleaned_data.get('nume')
        if nume_introdus:
            # Folosim o expresie regulată pentru a bloca caracterele speciale ciudate
            if re.search(r'[@#$%^&*_{}\[\]<>\/\\|]', nume_introdus):
                # Aruncăm o eroare cu mesajul nostru personalizat
                raise forms.ValidationError("Te rugăm să nu folosești caractere speciale (precum @, #, $, <, >) în numele produsului căutat.")
        return nume_introdus

    # Validările 2 și 3: Verificăm interdependența între mai multe câmpuri folosind metoda clean() generală
    def clean(self):
        # Apelăm clean()-ul de bază al lui Django
        cleaned_data = super().clean()
        
        # Extragem valorile
        pret_min = cleaned_data.get("pret_min")
        pret_max = cleaned_data.get("pret_max")
        greutate_min = cleaned_data.get("greutate_min")
        greutate_max = cleaned_data.get("greutate_max")

        # Validarea 2: Prețul minim vs Prețul maxim
        if pret_min is not None and pret_max is not None:
            if pret_max < pret_min:
                # Asociem eroarea specific câmpului 'pret_max'
                self.add_error('pret_max', "Eroare logică: Prețul maxim nu poate fi mai mic decât prețul minim introdus!")
                
        # Validarea 3: Greutatea minimă vs Greutatea maximă
        if greutate_min is not None and greutate_max is not None:
            if greutate_max < greutate_min:
                # Asociem eroarea specific câmpului 'greutate_max'
                self.add_error('greutate_max', "Eroare logică: Ai setat o greutate maximă mai mică decât cea minimă!")
                
        return cleaned_data
    

# --- FUNCȚII DE VALIDARE PERSONALIZATE ---

def valideaza_varsta_majora(value):
    # value este de tip datetime.date
    azi = date.today()
    # Calculăm vârsta (scădem 1 an dacă nu a fost încă ziua de naștere anul acesta)
    varsta = azi.year - value.year - ((azi.month, azi.day) < (value.month, value.day))
    if varsta < 18:
        raise ValidationError("Expeditorul trebuie să aibă peste 18 ani pentru a trimite un mesaj.")

def valideaza_numar_cuvinte(value):
    # \w+ găsește secvențe alfanumerice. Folosim [a-zA-Z0-9]+ pentru a fi strict alfanumeric
    cuvinte = re.findall(r'[a-zA-Z0-9ăâîșțĂÂÎȘȚ]+', value)
    if len(cuvinte) < 5 or len(cuvinte) > 100:
        raise ValidationError(f"Mesajul trebuie să conțină între 5 și 100 de cuvinte. (Ai introdus {len(cuvinte)})")

def valideaza_lungime_cuvinte(value):
    cuvinte = re.findall(r'[a-zA-Z0-9ăâîșțĂÂÎȘȚ]+', value)
    for cuvant in cuvinte:
        if len(cuvant) > 15:
            raise ValidationError(f"Niciun cuvânt nu poate depăși 15 caractere. (Cuvântul '{cuvant}' este prea lung).")

def valideaza_fara_linkuri(value):
    # Căutăm orice cuvânt care începe cu http:// sau https://
    if re.search(r'\bhttps?://', value):
        raise ValidationError("Textul nu poate conține linkuri (http:// sau https://).")

def valideaza_tip_mesaj(value):
    if value == 'neselectat':
        raise ValidationError("Te rugăm să selectezi un tip de mesaj valid din listă.")

def valideaza_cnp_cifre(value):
    if not value.isdigit():
        raise ValidationError("CNP-ul trebuie să conțină doar cifre.")

def valideaza_cnp_format_data(value):
    # value are deja 13 caractere (datorita min_length=13) si doar cifre (din validarea anterioara)
    prima_cifra = value[0]
    if prima_cifra not in ['1', '2', '5', '6']:
        raise ValidationError("CNP-ul trebuie să înceapă cu 1, 2, 5 sau 6.")
    
    # Extragem anul, luna, ziua (AALLZZ)
    an_format = int(value[1:3])
    luna = int(value[3:5])
    zi = int(value[5:7])
    
    # Determinăm anul complet pe baza primei cifre
    an_complet = 1900 + an_format if prima_cifra in ['1', '2'] else 2000 + an_format
    
    # Verificăm dacă data este validă (ex: respingem 30 februarie)
    try:
        date(an_complet, luna, zi)
    except ValueError:
        raise ValidationError(f"Cifrele {value[1:7]} din CNP nu formează o dată calendaristică validă.")

def valideaza_email_domeniu(value):
    domeniu = value.split('@')[-1].lower()
    if domeniu in ['guerillamail.com', 'yopmail.com']:
        raise ValidationError(f"Nu acceptăm adrese de e-mail temporare ({domeniu}).")

def valideaza_format_text(value):
    # Verifică dacă începe cu literă mare și conține DOAR litere, spații și cratime
    if not re.match(r'^[A-ZĂÂÎȘȚ][a-zA-ZĂÂÎȘȚăâîșț \-]*$', value):
        raise ValidationError("Textul trebuie să înceapă cu literă mare și să conțină doar litere, spații și cratime.")

def valideaza_majuscula_dupa_separator(value):
    # Caută un spațiu sau cratimă urmat de o literă mică
    if re.search(r'[ \-][a-zăâîșț]', value):
        raise ValidationError("După fiecare spațiu sau cratimă trebuie să urmeze o literă mare.")


class ContactForm(forms.Form):
    nume = forms.CharField(
        max_length=10, required=True, label="Nume",
        validators=[valideaza_format_text, valideaza_majuscula_dupa_separator]
    )
    
    # La prenume, dacă este lăsat gol (required=False), Django nu va apela validatorii, 
    # deci nu vom avea erori pe un câmp opțional gol!
    prenume = forms.CharField(
        max_length=10, required=False, label="Prenume",
        validators=[valideaza_format_text, valideaza_majuscula_dupa_separator]
    )
    
    cnp = forms.CharField(
        min_length=13, max_length=13, required=False, label="CNP",
        validators=[valideaza_cnp_cifre, valideaza_cnp_format_data]
    )
    
    data_nasterii = forms.DateField(
        required=True, label="Data nașterii",
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[valideaza_varsta_majora]
    )
    
    email = forms.EmailField(
        required=True, label="E-mail",
        validators=[valideaza_email_domeniu]
    )
    
    confirmare_email = forms.EmailField(
        required=True, label="Confirmare e-mail"
    )
    
    TIP_MESAJ_CHOICES = [
        ('neselectat', 'Neselectat'), ('reclamatie', 'Reclamație'),
        ('intrebare', 'Întrebare'), ('review', 'Review'),
        ('cerere', 'Cerere'), ('programare', 'Programare')
    ]
    tip_mesaj = forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES, initial='neselectat', required=True, label="Tip mesaj",
        validators=[valideaza_tip_mesaj]
    )
    
    subiect = forms.CharField(
        max_length=100, required=True, label="Subiect",
        validators=[valideaza_format_text, valideaza_fara_linkuri]
    )
    
    minim_zile_asteptare = forms.IntegerField(
        min_value=1, max_value=30, required=True, label="Minim zile așteptare",
        help_text="Pentru review-uri/cereri minimul de zile de așeptare trebuie setat de la 4 încolo iar pentru cereri/întrebări de la 2 încolo. Maximul e 30."
    )
    
    mesaj = forms.CharField(
        required=True, label="Mesaj",
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Scrie mesajul tău aici...'}),
        validators=[valideaza_numar_cuvinte, valideaza_lungime_cuvinte, valideaza_fara_linkuri]
    )
    def clean(self):
        # Apelăm metoda de bază pentru a prelua dicționarul cu toate datele valide de până acum
        cleaned_data = super().clean()

        # Extragem valorile pentru a le putea compara
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        nume = cleaned_data.get('nume')
        mesaj = cleaned_data.get('mesaj')
        tip_mesaj = cleaned_data.get('tip_mesaj')
        zile_asteptare = cleaned_data.get('minim_zile_asteptare')
        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')

        # 1. Validare Email vs Confirmare Email
        if email and confirmare_email and email != confirmare_email:
            # Folosim add_error pentru a afișa eroarea fix sub câmpul greșit
            self.add_error('confirmare_email', "Adresele de e-mail nu coincid! Te rugăm să verifici.")

        # 2. Validare Semnătură (Ultimul cuvânt din mesaj trebuie să fie numele)
        if nume and mesaj:
            import re
            # Extragem toate cuvintele din mesaj
            cuvinte_mesaj = re.findall(r'[a-zA-Z0-9ăâîșțĂÂÎȘȚ]+', mesaj)
            
            if cuvinte_mesaj:
                ultimul_cuvant = cuvinte_mesaj[-1]
                # Le comparăm transformate în litere mici pentru a nu depinde de majuscule
                if ultimul_cuvant.lower() != nume.lower():
                    self.add_error('mesaj', f"Mesajul trebuie să se încheie cu numele tău ('{nume}') pe post de semnătură.")

        # 3. Validare Zile Așteptare vs Tip Mesaj
        if tip_mesaj and zile_asteptare is not None:
            if tip_mesaj in ['review', 'cerere'] and zile_asteptare < 4:
                self.add_error('minim_zile_asteptare', f"Pentru {tip_mesaj} numărul minim de zile de așteptare este de 4.")
            elif tip_mesaj == 'intrebare' and zile_asteptare < 2:
                self.add_error('minim_zile_asteptare', "Pentru o întrebare numărul minim de zile de așteptare este de 2.")

        # 4. Validare CNP vs Data Nașterii
        if cnp and data_nasterii:
            # Extragem anul, luna și ziua din CNP
            prima_cifra = cnp[0]
            an_cnp = int(cnp[1:3])
            luna_cnp = int(cnp[3:5])
            zi_cnp = int(cnp[5:7])
            
            # Reconstruim anul complet pe baza primei cifre din CNP (1/2 = 1900+, 5/6 = 2000+)
            if prima_cifra in ['1', '2']:
                an_complet_cnp = 1900 + an_cnp
            elif prima_cifra in ['5', '6']:
                an_complet_cnp = 2000 + an_cnp
            else:
                an_complet_cnp = 0 # Fallback în caz că validatorul individual a lăsat ceva să scape
                
            # Verificăm dacă data extrasă din CNP se potrivește cu data din calendar
            if (data_nasterii.year != an_complet_cnp or 
                data_nasterii.month != luna_cnp or 
                data_nasterii.day != zi_cnp):
                
                self.add_error('cnp', "CNP-ul introdus nu corespunde cu data nașterii selectată în calendar.")

        # Returnăm dicționarul curățat la final (obligatoriu în Django)
        return cleaned_data
    
    
    

def valideaza_fara_caractere_speciale(value):
    """Verifică să nu existe caractere dubioase în text."""
    if re.search(r'[@#$%^&*_{}\[\]<>\\|]', str(value)):
        # Mesaj personalizat
        raise ValidationError("Textul conține caractere speciale nepermise (ex: @, #, $, <, >). Te rugăm să folosești doar litere, cifre și punctuație normală.")

def valideaza_primul_caracter_majuscula(value):
    """Verifică dacă primul caracter este literă mare."""
    if not str(value)[0].isupper():
        # Mesaj personalizat
        raise ValidationError("Acest câmp trebuie să înceapă obligatoriu cu literă mare!")
    

class ProdusForm(forms.ModelForm):
    # Câmpurile declarate explicit (aici definim deja label și widget)
    nume = forms.CharField(
        label="Denumire Comercială Produs",
        validators=[valideaza_fara_caractere_speciale, valideaza_primul_caracter_majuscula],
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Nike Air Max'})
    )
    
    descriere = forms.CharField(
        label="Descriere Detaliată (pentru clienți)",
        validators=[valideaza_fara_caractere_speciale],
        help_text="Includeți detalii despre material, cusături și recomandări de întreținere (minim 5 cuvinte).",
        widget=forms.Textarea(attrs={'rows': 3})
    )

    # --- INPUTURILE ADIȚIONALE ---
    pret_furnizor = forms.DecimalField(
        label="Preț de achiziție de la furnizor (RON)", 
        min_value=1,
        help_text="Introduceți prețul brut unitar facturat de producător, fără taxe adiționale.",
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 150.00'})
    )
    adaos_procent = forms.DecimalField(
        label="Adaos Comercial Dorit (%)", 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 40'})
    )
    greutate_stang = forms.FloatField(
        label="Greutate pantof stâng (g)", 
        min_value=10
    )
    greutate_drept = forms.FloatField(
        label="Greutate pantof drept (g)", 
        min_value=10
    )
    
    class Meta:
        model = Produs
        fields = ['nume', 'descriere', 'categorie']
        
        # Lăsăm aici doar etichetele pentru câmpurile care NU sunt definite explicit mai sus
        labels = {
            'categorie': 'Categoria de Încălțăminte'
        }
        # Nu mai avem nevoie de dicționarul widgets aici, pentru că le-am definit deja mai sus!

    # --- VALIDĂRI INTERNE ---

    def clean_nume(self):
        nume = self.cleaned_data.get('nume')
        # Am șters verificarea majusculei de aici (o face deja funcția externă). Lăsăm doar lungimea.
        if len(nume) < 3:
            raise ValidationError("Denumirea este prea scurtă (minim 3 caractere).")
        return nume

    def clean_descriere(self):
        descriere = self.cleaned_data.get('descriere')
        cuvinte = re.findall(r'[a-zA-Z0-9ăâîșțĂÂÎȘȚ]+', descriere)
        if len(cuvinte) < 5:
            raise ValidationError(f"Descrierea este prea sumară. Trebuie să conțină minim 5 cuvinte (tu ai introdus {len(cuvinte)}).")
        return descriere

    def clean_adaos_procent(self):
        adaos = self.cleaned_data.get('adaos_procent')
        if adaos > 1000:
            raise ValidationError("Eroare de sistem: Adaosul comercial nu poate depăși limita maximă admisă de 1000%.")
        return adaos

    def clean(self):
        cleaned_data = super().clean()
        
        g_stang = cleaned_data.get('greutate_stang')
        g_drept = cleaned_data.get('greutate_drept')
        
        if g_stang is not None and g_drept is not None:
            diferenta = abs(g_stang - g_drept)
            
            if diferenta > 15:
                self.add_error(
                    'greutate_drept', 
                    f"Diferența de greutate între pantofi este prea mare ({diferenta}g)! Pantoful stâng are {g_stang}g, iar cel drept {g_drept}g. Vă rugăm să verificați datele introduse."
                )

        return cleaned_data
    
    
class InregistrareForm(UserCreationForm):
    # Suprascriem data_nasterii pentru a folosi widget-ul de calendar html5
    data_nasterii = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Data nașterii"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Includem câmpurile implicite pe care le dorim + cele 5 create de noi
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 
            'telefon', 'adresa', 'judet', 'cnp', 'data_nasterii'
        )

    # --- VALIDĂRI PENTRU MINIM 3 DIN CELE 5 CÂMPURI ---

    # Validarea 1: Telefonul să conțină doar cifre și să aibă minim 10 caractere
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if telefon:
            if not telefon.isdigit():
                raise ValidationError("Numărul de telefon trebuie să conțină exclusiv cifre.")
            if len(telefon) < 10:
                raise ValidationError("Numărul de telefon este prea scurt (minim 10 cifre).")
        return telefon

    # Validarea 2: CNP-ul să aibă fix 13 caractere și să conțină doar cifre
    def clean_cnp(self):
        cnp = self.cleaned_data.get('cnp')
        if cnp:
            if not cnp.isdigit():
                raise ValidationError("CNP-ul trebuie să conțină doar cifre.")
            if len(cnp) != 13:
                raise ValidationError(f"CNP-ul trebuie să aibă exact 13 cifre (tu ai introdus {len(cnp)}).")
        return cnp

    # Validarea 3: Utilizatorul trebuie să fie major
    def clean_data_nasterii(self):
        data = self.cleaned_data.get('data_nasterii')
        if data:
            azi = date.today()
            varsta = azi.year - data.year - ((azi.month, azi.day) < (data.month, data.day))
            if varsta < 18:
                raise ValidationError("Trebuie să ai minim 18 ani pentru a te putea înregistra pe platformă.")
        return data
    
    

class CustomLoginForm(AuthenticationForm):
    ramai_logat = forms.BooleanField(
        required=False, 
        label="Păstrează-mă logat pe site (24 ore)",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-custom'})
    )