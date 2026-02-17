from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns =[
    path('', views.index, name="index"), 
    path("info/", views.info, name="info"),
    path("log/", views.log, name="log"),
    path("data/", views.afis_data, name ="afis_data"),
    path('despre/', views.despre, name='despre'),
    path('cos_virtual/', views.in_lucru_view, name='cos_virtual'),
    path('faq/', views.in_lucru_view, name='faq'),
    path('termeni/', views.in_lucru_view, name='termeni'),
    path('adauga-produs/', views.adauga_produs_view, name='adauga_produs'),
    path('produse/', views.produse_view, name='produse'),
    path('produs/<int:id_produs>/', views.produs_detaliu, name='produs_detaliu'),
    path('categorii/<str:nume_categorie>/', views.categorie_view, name='categorie_detaliu'),
    path('contact/', views.contact_view, name='contact'),
    path('inregistrare/', views.inregistrare_view, name='inregistrare'),
    path('confirma_mail/<str:cod>/', views.confirma_mail_view, name='confirma_mail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.profil_view, name='profil'),
    path('promotii/', views.promotii_view, name='promotii'),
    path('schimba-parola/', auth_views.PasswordChangeView.as_view(
        template_name='schimba_parola.html',
        success_url=reverse_lazy('profil') 
    ), name='schimba_parola'),
]
