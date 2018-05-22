from django.urls import path
from . import views

app_name = 'caprino.animais'
urlpatterns = [

    path('novo_animal/', views.CreateAnimal, name='Novo_Animal'),
    path('apaga_animal/<int:pk>/', views.DeleteAnimal, name='Apaga_Animal'),
    path('mostra_animal/', views.MostraAnimal, name='Mostra_Animal'),
    path('atualiza_animal/<int:pk>', views.UpdateAnimal, name='Atualiza_Animal'),

    path('nova_cobertura/', views.CreateCobertura, name='Nova_Cobertura'),
    path('mostra_coberturas/', views.MostraCoberturas, name='Mostra_Coberturas'),
    path('delete_cobertura/<int:pk>/', views.DeleteCobertura, name='Delete_Cobertura'),
    path('atualiza_cobertura/<int:pk>', views.UpdateCobertura, name='Atualiza_Cobertura'),

    path('nova_producao/', views.CreateProducoes, name='Nova_Producao'),
    path('mostra_producao/', views.MostraProducao, name='Mostra_Producao'),
    path('delete_producao/<int:pk>/', views.DeleteProducao, name='Delete_Producao'),
    path('atualiza_producao/<int:pk>', views.UpdateProducao, name='Atualiza_Producao'),

]
