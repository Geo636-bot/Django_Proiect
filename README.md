# Proiect Django

## Tema Proiectului: Magazin Online de Încălțăminte

Acest proiect reprezintă o platformă web interactivă și dinamică dedicată comercializării de încălțăminte. Scopul principal al aplicației este de a oferi utilizatorilor o experiență de navigare intuitivă, permițându-le să exploreze un catalog diversificat de produse (pantofi sport, eleganți, etc.), să filtreze avansat rezultatele și să interacționeze cu magazinul. 

La nivel tehnic, backend-ul este construit robust folosind framework-ul Python Django. Proiectul pune un accent puternic pe securitatea datelor, validarea complexă a formularelor, managementul sesiunilor și manipularea avansată a bazelor de date prin ORM-ul Django.

---

## 🚀 Funcționalități Noi Implementate

* **Sistem de Filtrare Avansat (`forms.Form`):**
  * Filtre complexe după nume, descriere, culori, intervale de preț (min/max), greutate, stoc și relații (Categorie, Brand, Material).
  * Menținerea stării filtrelor în timpul paginării și sortării (URL parameters retention).
  * Sistem inteligent de repaginare cu avertismente bazate pe `request.session`.
* **Securitate și Validări Personalizate:**
  * Validări încrucișate la nivel de formular (`clean()`) pentru prevenirea datelor logice eronate (ex: diferențe de greutate între pantofi, preț minim > preț maxim).
  * Securitate pe paginile de categorii (prevenirea manipulării câmpurilor ascunse/hidden din browser prin "Inspect Element").
  * Expresii regulate (Regex) pentru curățarea textelor, blocarea link-urilor și a caracterelor speciale.
* **Procesare și Salvare Fișiere (JSON):**
  * Formular de contact care nu salvează în baza de date, ci preprocesează informațiile (calculează vârsta în ani și luni, formatează spațiile, capitalizează literele).
  * Generarea de fișiere `.json` locale ce includ metadate (IP-ul utilizatorului, timestamp) și marcaje de urgență pe baza logicii de business.
* **Formulare Dinamice (`ModelForm`):**
  * Formular pentru adăugarea produselor noi care ascunde coloane din baza de date și le calculează matematic în spate (preț final bazat pe preț furnizor + adaos) folosind `commit=False`.
* **UI/UX Îmbunătățit:**
  * Integrare FontAwesome și coduri HEX în baza de date pentru generarea vizuală și dinamică a etichetelor de categorii.
  * Butoane inteligente de resetare a filtrelor cu confirmare JavaScript.

---

## 📂 Conținutul Platformei

Acest proiect conține următoarele pagini principale:

* **Prima pagină (Acasă):** Descrierea proiectului și oferte curente.
* **Categorii (`/categorii/`):** Listarea tuturor categoriilor de încălțăminte cu identitate vizuală proprie.
* **Catalog Produse (`/produse/`):** Catalogul complet, dotat cu paginare, sortare și panou lateral de filtrare complexă.
* **Adăugare Produs (`/adauga-produs/`):** Interfață protejată pentru angajați, destinată adăugării de inventar nou cu calcul automat de costuri.
* **Contact (`/contact/`):** Formular avansat de contact cu reguli stricte de validare (CNP valid, restricții de vârstă, blocare emailuri temporare).
* **Despre noi:** O scurtă istorie a magazinului și detalii despre echipa din spate.
* **Coș virtual / FAQ / Termeni și condiții:** Secțiuni standard pentru e-commerce.

---

## 🏗️ Structura Proiectului

Proiectul este construit folosind arhitectura standard Django (MVT - Model View Template), fiind structurat astfel:

```text
DJANGO_PROIECT/
└── Magazin_Incaltaminte/                 # Folderul rădăcină al proiectului
    ├── manage.py                         # Utilitarul de command-line Django
    ├── README.md                         # Documentația proiectului
    │
    ├── Magazin_Incaltaminte/             # Pachetul de configurare al proiectului
    │   ├── settings.py                   # Setările globale
    │   ├── urls.py                       # Rutarea principală a proiectului
    │   └── wsgi.py / asgi.py
    │
    └── Catalog_Produse/                  # Aplicația principală a magazinului
        ├── migrations/                   # Fisierele pentru migrarea bazei de date
        ├── Mesaje/                       # [NOU] Folder generat pentru salvarea cererilor de contact (.json)
        ├── admin.py                      # Configurarea interfeței de administrare
        ├── forms.py                      # [NOU] Logica tuturor formularelor (Filtrare, Contact, ModelForms)
        ├── models.py                     # Definirea structurii bazei de date (Modele)
        ├── urls.py                       # Rutele specifice aplicației
        ├── views.py                      # Logica aplicației (filtrare, procesare date, salvare)
        │
        ├── static/                       # Fișiere statice (CSS, JavaScript, Imagini)
        │   ├── css/style.css             
        │   └── imagini/                  
        │
        └── templates/                    # Șabloanele HTML
            ├── baza.html                 # Template-ul de bază (Header, Footer, Meniu)
            ├── index.html                # Prima pagină (Acasă)
            ├── produse.html              # [NOU] Catalogul cu filtre, sortare și paginare
            ├── contact.html              # [NOU] Formularul de contact cu afișare erori integrate
            ├── adauga_produs.html        # [NOU] Interfața de adăugare produse noi
            ├── toate_categoriile.html    # [NOU] Lista vizuală a categoriilor
            └── log.html / info.html / etc.
