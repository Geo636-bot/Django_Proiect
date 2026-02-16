from django.urls import path
from . import views

urlpatterns =[
    path("", views.index, name="index"), 
    path("info/", views.info, name="info"),
    path("log/", views.log, name="log"),
    path("data/", views.afis_data, name ="afis_data"),
    path('despre/', views.despre, name='despre'),
    path('produse/', views.in_lucru_view, name='produse'),
    path('cos_virtual/', views.in_lucru_view, name='cos_virtual'),
    path('contact/', views.in_lucru_view, name='contact'),
    path('faq/', views.in_lucru_view, name='faq'),
    path('termeni/', views.in_lucru_view, name='termeni'),
]
