from django.urls import path
from . import views

app_name = 'caprino.animais'
urlpatterns = [
    path('nova_cabra/', views.CreateCabra, name='Nova_Cabra'),
    path('mostra_cabras/', views.MostraCabras, name='Mostra_Cabras'),
    path('novo_bode/', views.CreateBode, name='Novo_Bode'),
    path('mostra_bodes/', views.MostraBodes, name='Mostra_Bodes'),
    path('nova_cobertura/', views.CreateCobertura, name='Nova_Cobertura'),

]
