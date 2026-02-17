import datetime
from django.shortcuts import get_object_or_404
from collections import Counter
from django.core.paginator import Paginator
from .models import Produs, Categorie
from django.http import HttpResponse
from .forms import FiltruProduseForm

LUNI = [
    "", 
    "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", 
    "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"
]
# Zilele saptamanii: Index 0 = Luni (now.weekday() returneaza 0-6)
ZILE_SAPTAMANA = [
    "Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"
]
LISTA_ACCESARI = []
ID_COUNTER = 0

def index(request):
    acces = Accesare(request) 
    context = {
        'descriere_proiect': "Acest proiect implementează un magazin online de încălțăminte.",
        'ip_utilizator': acces.ip_client
    }
    # Returnăm template-ul index.html
    return render(request, 'index.html', context)

def despre(request):
    acces = Accesare(request)
    return render(request, 'despre.html', {'ip_utilizator': acces.ip_client})

def in_lucru_view(request):
    acces = Accesare(request)
    return render(request, 'in_lucru.html', {'ip_utilizator': acces.ip_client})


def get_ip(request):
    """Obține adresa IP reală a clientului."""
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


def afis_data(request):
    now = datetime.datetime.now()

    zi_saptamana = ZILE_SAPTAMANA[now.weekday()]
    nume_luna = LUNI[now.month]
    
    data_formatata = f"{zi_saptamana}, {now.day} {nume_luna} {now.year}"
    timp_formatat = f"{now.hour:02}:{now.minute:02}:{now.second:02}" 
    
    # Verificăm ce parametri avem în URL (după semnul '?')
    if 'zi' in request.GET:
        data_ora_str = data_formatata
        titlu = "Ziua curentă (Server)"
    elif 'timp' in request.GET:
        data_ora_str = timp_formatat # Afișează strict ora
        titlu = "Ora curentă (Server)"
    else:
        # Dacă nu avem nici ?zi, nici ?timp, afișăm tot
        data_ora_str = f"{data_formatata}, ora {timp_formatat}"
        titlu = "Data și ora (Server)"
        
    html_output = f"""
    <section style="border-top: 2px solid #ddd; padding-top: 15px; margin-top: 20px;">
        <h2>{titlu}</h2>
        <p><strong>{data_ora_str}</strong></p>
    </section>
    """
    
    # Returnăm obiectul corect pentru Django
    return HttpResponse(html_output)


class Accesare:
    """Clasa pentru a înregistra datele fiecarei cereri de accesare."""
    
    # Variabilă de clasă (înlocuiește nevoia de 'global ID_COUNTER')
    _ID_COUNTER = 0 
    
    def __init__(self, request):
        Accesare._ID_COUNTER += 1
        self.id = Accesare._ID_COUNTER
        self.request = request 
        
        # Proprietățile clasei
        self.ip_client = get_ip(request) 
        self.data_accesare = datetime.datetime.now()
        
        # Salvăm instanța în lista globală
        LISTA_ACCESARI.append(self)

    def lista_parametri(self):
        """Returnează o listă de tupluri (cheie, valoare). Dacă valoarea lipsește, pune None."""
        # În Django, '?zi' va rezulta într-o valoare de tip string gol: ''
        # Folosim un if inline pentru a transforma '' în None
        return [(key, val if val != '' else None) for key, val in self.request.GET.items()]

    def url(self):
        """Returnează tot url-ul împreună cu query string (ex: /data?zi)."""
        return self.request.get_full_path()

    def data(self, format_string=None):
        """
        Dacă primește format_string, returnează data formatată ca string.
        Dacă nu, returnează direct obiectul de tip datetime.
        """
        if format_string:
            return self.data_accesare.strftime(format_string)
        return self.data_accesare

    def pagina(self):
        """Returnează doar calea paginii (ex: / sau /info), fără parametri."""
        return self.request.path


DESCRIERE_PROIECT = (
    "Acest proiect implementează un magazin online de încălțăminte. "
    "Obiectivul principal este de a oferi o platformă de e-commerce funcțională."
)




def info(request):
    """Pagina /info care afișează informații despre server și loghează accesarea."""
    
    # Creează instanța clasei Accesare
    acces = Accesare(request)
    
    # Reparam eroarea din codul initial: afis_data asteapta 'request', nu un string
    data_html = ""
    if "data" in request.GET:
        # Preluam continutul generat de afis_data si il decodam
        response_data = afis_data(request)
        data_html = response_data.content.decode('utf-8')
    
    # --- LOGICA NOUĂ PENTRU SECȚIUNEA PARAMETRI ---
    lista_parametri = acces.lista_parametri()
    nr_parametri = len(lista_parametri)
    # Extragem doar numele parametrilor (prima valoare din tuplu)
    nume_parametri = ", ".join([cheie for cheie, valoare in lista_parametri]) if nr_parametri > 0 else "Niciunul"
    
    response_html = f"""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Informații despre server</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #004d99; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h1>Informații despre server</h1>
        
        <section style="border: 1px solid #eee; padding: 15px; background-color: #f9f9f9;">
            <h2>Detalii accesare curentă</h2>
            <ul>
                <li><strong>ID Accesare:</strong> {acces.id}</li>
                <li><strong>IP Client:</strong> {acces.ip_client}</li>
                <li><strong>Pagina Accesată:</strong> {acces.pagina()}</li>
                <li><strong>URL Complet:</strong> {acces.url()}</li>
            </ul>
        </section>

        <section style="border: 1px solid #ccc; padding: 15px; margin-top: 20px; background-color: #eef7e6;">
            <h2>Parametri</h2>
            <p>Număr parametri primiți: <strong>{nr_parametri}</strong></p>
            <p>Numele acestora: <strong>{nume_parametri}</strong></p>
        </section>

        {data_html}
    </body>
    </html>
    """
    return HttpResponse(response_html)

def log(request):
    """
    Pagina /log: afișează cererile recente, filtrează, permite afișare tip listă sau tabel dinamic,
    și afișează statistici cu cea mai (putin) accesata pagina.
    """
    acces_curent = Accesare(request)
    k_totale = len(LISTA_ACCESARI)
    mesaj_eroare = ""
    accesari_de_afisat = LISTA_ACCESARI
    
    # --- Secțiunea 1: Extragerea și Validarea Parametrilor ---
    
    nr_accesari_html = ""
    accesari_param = request.GET.get("accesari")
    mesaj_eroare_final = "" # <-- Variabilă nouă pentru eroarea de la final
    
    # Parametrul 'accesari=nr'
    if accesari_param == "nr":
        nr_accesari_html = f"""
            <section style="background-color: #e6f7ff; padding: 10px; border: 1px solid #b3e0ff;">
                <h2>Număr Total de Accesări</h2>
                <p>De la pornirea serverului, s-au înregistrat <strong>{k_totale}</strong> accesări.</p>
            </section>
        """

    # Parametrul 'ultimele'
    n_cerute = request.GET.get("ultimele")
    if n_cerute is not None:
        try:
            n_cerute = int(n_cerute)
            if n_cerute <= 0: raise ValueError
            
            if n_cerute > k_totale:
                # Mesajul exact cerut, salvat pentru a fi afișat la final
                mesaj_eroare_final = f"<p style='color:orange; font-weight: bold;'>Exista doar {k_totale} accesari fata de {n_cerute} accesari cerute</p>"
                accesari_de_afisat = LISTA_ACCESARI # Afișăm toate accesările
            else:
                accesari_de_afisat = LISTA_ACCESARI[-n_cerute:] # Afișăm doar ultimele n
        except ValueError:
            mesaj_eroare += f"<p style='color:red;'>Eroare: Valoarea '{request.GET.get('ultimele')}' nu este o valoare numerică întreagă validă.</p>"
    
    # --- Secțiunea 2: Logica 'iduri' și 'dubluri' ---
    iduri_list = request.GET.getlist('iduri')
    
    # Verificăm dacă a fost furnizat cel puțin un parametru 'iduri'
    if iduri_list:
        # Preluăm valoarea lui dubluri (implicit 'false')
        dubluri_permise = request.GET.get("dubluri", "false").lower() == "true"
        
        iduri_cerute = []
        iduri_vazute = set() # Folosim un set pentru o verificare mai rapidă a dublurilor
        
        for id_group in iduri_list:
            # id_group poate fi "2,3" sau "4,2,1"
            for id_str in id_group.split(','):
                id_str = id_str.strip()
                if not id_str:
                    continue # Sărim peste valorile goale (ex: iduri=2,,3)
                
                try:
                    current_id = int(id_str)
                    
                    # Verificăm dacă permitem dubluri SAU dacă ID-ul nu a mai fost adăugat
                    if dubluri_permise or current_id not in iduri_vazute:
                        
                        # Căutăm obiectul în LISTA_ACCESARI
                        accesare_obiect = next((a for a in LISTA_ACCESARI if a.id == current_id), None)
                        
                        if accesare_obiect:
                            iduri_cerute.append(accesare_obiect)
                            iduri_vazute.add(current_id) # Îl marcăm ca 'văzut'
                        else:
                            mesaj_eroare += f"<p style='color:red;'>Eroare: Accesarea cu ID-ul {current_id} nu există.</p>"
                except ValueError:
                    mesaj_eroare += f"<p style='color:red;'>Eroare: Valoarea '{id_str}' nu este un ID valid.</p>"
        
        # Dacă s-au cerut id-uri, afișăm doar lista construită
        accesari_de_afisat = iduri_cerute


    # --- Secțiunea 3: Generarea conținutului (Listă sau Tabel) ---
    continut_afisaj = ""

    # TASK A: Afișare sub formă de listă neordonată pentru accesari=detalii
    if accesari_param == "detalii":
        continut_afisaj += "<div style='background-color: #fff3e6; padding: 15px; margin-top: 15px; border: 1px solid #ffd480;'>"
        continut_afisaj += "<h2>Detalii Accesări (Dată și Oră)</h2>"
        continut_afisaj += "<ul>"
        for acces in accesari_de_afisat:
            # Folosim metoda data() cu un format lizibil pentru data si ora
            continut_afisaj += f"<li>{acces.data('%d %b %Y, %H:%M:%S')}</li>"
        continut_afisaj += "</ul></div>"
        
    # TASK B: Afișarea în format Tabel dinamic
    tabel_param = request.GET.get("tabel")
    
    if tabel_param is not None: # Dacă parametrul 'tabel' este prezent în query string
        # Definim dicționarul de proprietăți (nume coloană -> cum extragem valoarea)
        proprietati_disponibile = {
            'id': lambda a: str(a.id),
            'ip': lambda a: a.ip_client,
            'data': lambda a: a.data('%Y-%m-%d %H:%M:%S'),
            'pagina': lambda a: a.pagina(),
            'url': lambda a: a.url()
        }
        
        # Stabilim ce coloane afișăm
        if tabel_param == "tot":
            coloane = list(proprietati_disponibile.keys()) # Toate
        else:
            # Extragem coloanele cerute (ex: 'id,url') și ignorăm spațiile/literele mari
            coloane_cerute = [c.strip().lower() for c in tabel_param.split(',')]
            # Le păstrăm doar pe cele valide (care există în dicționar)
            coloane = [c for c in coloane_cerute if c in proprietati_disponibile]
        
        # Dacă avem cel puțin o coloană validă, generăm tabelul
        if coloane:
            continut_afisaj += "<h2 style='margin-top: 30px;'>Date Accesări (Tabel)</h2>"
            continut_afisaj += "<table><thead><tr>"
            
            # Generăm capul de tabel
            for col in coloane:
                continut_afisaj += f"<th>{col.upper()}</th>"
            continut_afisaj += "</tr></thead><tbody>"
            
            # Generăm rândurile
            for acces in accesari_de_afisat:
                continut_afisaj += "<tr>"
                for col in coloane:
                    # Apelăm funcția lambda corespunzătoare coloanei
                    continut_afisaj += f"<td>{proprietati_disponibile[col](acces)}</td>"
                continut_afisaj += "</tr>"
            
            continut_afisaj += "</tbody></table>"
        else:
            mesaj_eroare += f"<p style='color:orange;'>Nicio coloană validă nu a fost specificată pentru tabel.</p>"

    # --- Secțiunea 4: Statistici Pagini (Cea mai mult/puțin accesată) ---
    statistici_html = ""
    
    # Ne asigurăm că avem cel puțin o accesare înregistrată
    if LISTA_ACCESARI:
        # Extragem o listă doar cu numele paginilor accesate (ex: ['/', '/info', '/', '/log'])
        toate_paginile = [a.pagina() for a in LISTA_ACCESARI]
        
        # Numărăm de câte ori apare fiecare pagină
        contor_pagini = Counter(toate_paginile)
        
        # Găsim numărul minim și maxim de accesări
        minim_accesari = min(contor_pagini.values())
        maxim_accesari = max(contor_pagini.values())
        
        # Găsim toate paginile care au acest număr minim/maxim (astfel tratăm egalitățile)
        pagini_minime = [pag for pag, count in contor_pagini.items() if count == minim_accesari]
        pagini_maxime = [pag for pag, count in contor_pagini.items() if count == maxim_accesari]
        
        # Le transformăm în string-uri separate prin virgulă pentru afișare
        str_pagini_min = ", ".join(f"<code>{p}</code>" for p in pagini_minime)
        str_pagini_max = ", ".join(f"<code>{p}</code>" for p in pagini_maxime)
        
        statistici_html = f"""
        <section style="margin-top: 30px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #CC3300;">
            <h3>Statistici de Accesare</h3>
            <ul>
                <li>Pagina <strong>cea mai puțin</strong> accesată: {str_pagini_min} ({minim_accesari} accesări)</li>
                <li>Pagina <strong>cea mai mult</strong> accesată: {str_pagini_max} ({maxim_accesari} accesări)</li>
            </ul>
        </section>
        """
    # --- Secțiunea 5: Returnarea HTML-ului Final ---
    response_html = f"""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Jurnal de accesare (Log)</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #CC3300; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            ul {{ list-style-type: square; }}
        </style>
    </head>
    <body>
        <h1>Jurnal de accesare ({k_totale} cereri totale)</h1>
        
        {nr_accesari_html}
        {mesaj_eroare}

        {continut_afisaj}
        
        {statistici_html}
        
        {mesaj_eroare_final}
        
        <p><i>Această cerere curentă (ID: {acces_curent.id}) este inclusă în log.</i></p>
    </body>
    </html>
    """
    
    return HttpResponse(response_html)

def produse_view(request):
    """Afișează produsele cu paginare, sortare și FILTRARE avansată."""
    
    # 1. Inițializăm lista cu toate produsele
    lista_produse = Produs.objects.all()
    
    # 2. Instanțiem formularul cu datele din cererea GET
    form = FiltruProduseForm(request.GET)
    
    # 3. Dacă formularul este valid, extragem datele și aplicăm filtrele rând pe rând
    if form.is_valid():
        nume = form.cleaned_data.get('nume')
        descriere = form.cleaned_data.get('descriere')
        pret_min = form.cleaned_data.get('pret_min')
        pret_max = form.cleaned_data.get('pret_max')
        greutate_min = form.cleaned_data.get('greutate_min')
        greutate_max = form.cleaned_data.get('greutate_max')
        culoare_principala = form.cleaned_data.get('culoare_principala')
        in_stoc = form.cleaned_data.get('in_stoc')
        categorie = form.cleaned_data.get('categorie')
        brand = form.cleaned_data.get('brand')
        material = form.cleaned_data.get('material')
        
        # Aplicăm filtrele (folosim icontains pentru o potrivire parțială și insensibilă la majuscule)
        if nume:
            lista_produse = lista_produse.filter(nume__icontains=nume)
        if descriere:
            lista_produse = lista_produse.filter(descriere__icontains=descriere)
        if culoare_principala:
            lista_produse = lista_produse.filter(culoare_principala__icontains=culoare_principala)
            
        # Filtre de minim/maxim
        if pret_min is not None:
            lista_produse = lista_produse.filter(pret__gte=pret_min) # gte = Greater Than or Equal
        if pret_max is not None:
            lista_produse = lista_produse.filter(pret__lte=pret_max) # lte = Less Than or Equal
        if greutate_min is not None:
            lista_produse = lista_produse.filter(greutate__gte=greutate_min)
        if greutate_max is not None:
            lista_produse = lista_produse.filter(greutate__lte=greutate_max)
            
        # Filtre exacte
        if in_stoc == '1':
            lista_produse = lista_produse.filter(in_stoc=True)
        elif in_stoc == '0':
            lista_produse = lista_produse.filter(in_stoc=False)
            
        # Filtre pentru relații (Foreign Keys)
        if categorie:
            lista_produse = lista_produse.filter(categorie=categorie)
        if brand:
            lista_produse = lista_produse.filter(brand=brand)
        if material:
            lista_produse = lista_produse.filter(material=material)

    # 4. Păstrăm sortarea de dinainte
    sort_param = request.GET.get('sort', '')
    if sort_param == 'a':
        lista_produse = lista_produse.order_by('pret')
    elif sort_param == 'd':
        lista_produse = lista_produse.order_by('-pret')
    else:
        lista_produse = lista_produse.order_by('-data_adaugarii')

    # --- GENERARE URL-URI PENTRU A NU PIERDE FILTRELE / SORTAREA ---
    # 1. Pentru paginare: Păstrăm tot (filtre+sortare), dar scoatem 'page' vechi
    query_paginare = request.GET.copy()
    if 'page' in query_paginare:
        del query_paginare['page']
    url_paginare = query_paginare.urlencode()

    # 2. Pentru butoanele de sortare: Păstrăm filtrele, dar scoatem 'sort' și resetăm la pagina 1
    query_sortare = request.GET.copy()
    if 'sort' in query_sortare:
        del query_sortare['sort']
    if 'page' in query_sortare:
        del query_sortare['page']
    url_sortare = query_sortare.urlencode()

    # --- PAGINARE ---
    paginator = Paginator(lista_produse, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'sort_param': sort_param,
        'form': form,
        'url_paginare': url_paginare,
        'url_sortare': url_sortare
    }
    return render(request, 'produse.html', context)


def produs_detaliu(request, id_produs):
    """Afișează detaliile unui singur produs."""
    try:
        # Încercăm să găsim produsul cu ID-ul cerut în URL
        produs_cerut = Produs.objects.get(id_incaltaminte=id_produs)
        
        # Dacă îl găsește, randează pagina produsului
        return render(request, 'produs.html', {'produs': produs_cerut})
        
    except Produs.DoesNotExist:
        # Dacă produsul nu există în baza de date, afișăm pagina de eroare
        return render(request, 'eroare.html', status=404)
    
from django.shortcuts import render, get_object_or_404
# ... restul importurilor tale

def categorie_view(request, nume_categorie):
    
    # 1. Găsim categoria pe baza numelui din URL (sau dăm eroare 404 dacă nu există)
    categorie_curenta = get_object_or_404(Categorie, nume_categorie=nume_categorie)
    
    # 2. Filtrăm produsele CA SĂ LE AFIȘĂM DOAR PE CELE DIN ACEASTĂ CATEGORIE
    lista_produse = Produs.objects.filter(categorie=categorie_curenta)
    
    # 3. Păstrăm funcționalitatea de sortare (opțional, dar recomandat)
    sort_param = request.GET.get('sort')
    if sort_param == 'a':
        lista_produse = lista_produse.order_by('pret')
    elif sort_param == 'd':
        lista_produse = lista_produse.order_by('-pret')
    else:
        lista_produse = lista_produse.order_by('-data_adaugarii')
        sort_param = ''
        
    # 4. Paginarea (5 pe pagină)
    paginator = Paginator(lista_produse, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Trimitem categoria curentă în context pentru a-i afișa detaliile în template
    context = {
        'categorie_curenta': categorie_curenta,
        'page_obj': page_obj,
        'sort_param': sort_param
    }
    return render(request, 'produse.html', context) # REFOLOSIM TEMPLATE-UL!