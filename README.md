# Proiect E-Commerce Django

## Tema Proiectului: Magazin Online de Încălțăminte

Acest proiect reprezintă o platformă web interactivă dedicată comercializării de încălțăminte. Scopul principal al aplicației este de a oferi utilizatorilor o experiență de navigare intuitivă, permițându-le să exploreze un catalog diversificat de produse (pantofi sport, eleganți, etc.), să afle informații despre istoricul și echipa magazinului, dar și să interacționeze cu funcționalități specifice precum coșul virtual și paginile de contact. La nivel tehnic, backend-ul este construit robust folosind framework-ul Python Django, incluzând un sistem personalizat de logare și monitorizare a accesărilor pentru fiecare pagină a site-ului.

---

## Conținut
Acest proiect conține următoarele pagini principale:

* **Prima pagină (Acasă):** Pagina principală a magazinului. Conține descrierea proiectului, categoriile principale de produse și ofertele curente.
* **Despre noi:** O scurtă istorie a magazinului nostru și detalii despre echipa din spate.
* **Produse:** Catalogul complet unde vizitatorii pot vizualiza încălțămintea disponibilă.
* **Contact:** Formularul și datele de contact pentru suport clienți.
* **Coș virtual:** Secțiunea unde utilizatorii își pot revizui produsele adăugate înainte de finalizarea comenzii.
* **FAQ (Întrebări frecvente):** Răspunsuri la cele mai comune curiozități ale clienților noștri.
* **Termeni și condiții:** Detaliile legale privind utilizarea magazinului online.

## Structura Proiectului

Proiectul este construit folosind framework-ul Django și respectă o arhitectură standard, fiind structurat astfel:

```text
DJANGO_PROIECT/
└── Magazin_Incaltaminte/                 # Folderul rădăcină al proiectului
    ├── manage.py                         # Utilitarul de command-line Django
    ├── README.md                         # Documentația proiectului
    │
    ├── Magazin_Incaltaminte/             # Pachetul de configurare al proiectului
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py                   # Setările globale (inclusiv configurarea static/templates)
    │   ├── urls.py                       # Rutarea principală a proiectului
    │   └── wsgi.py
    │
    └── Catalog_Produse/                  # Aplicația principală a magazinului
        ├── migrations/                   # Fisierele pentru migrarea bazei de date
        ├── __init__.py
        ├── admin.py                      # Configurarea interfeței de administrare
        ├── apps.py
        ├── models.py                     # Definirea structurii bazei de date (Modele)
        ├── tests.py                      # Teste unitare
        ├── urls.py                       # Rutele specifice aplicației
        ├── views.py                      # Logica din spate (funcțiile care randează paginile)
        │
        ├── static/                       # Fișiere statice (CSS, JavaScript, Imagini)
        │   ├── css/
        │   │   └── style.css             # Fișierul CSS pentru design (inclusiv meniul derulant)
        │   └── imagini/
        │       ├── incaltaminte.jpg      # Imagine pentru prima pagină
        │       └── echipa.jpg            # Imagine pentru pagina Despre Noi
        │
        └── templates/                    # Șabloanele HTML
            ├── baza.html                 # Template-ul de bază (Header, Footer, Meniu)
            ├── index.html                # Prima pagină (Acasă)
            ├── despre.html               # Pagina Despre Noi
            ├── in_lucru.html             # Pagina generică pentru secțiunile nefinalizate
            ├── info.html                 # Pagina cu detalii despre server și request curent
            └── log.html                  # Pagina cu istoricul de accesări
