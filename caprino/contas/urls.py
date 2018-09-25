from django.urls import path
from . import views

app_name = 'caprino.contas'
urlpatterns = [
    path('entrar/', views.Entrar, name='Entrar'),
    path('sair/', views.Sair, name='Sair'),

    path('novo_usuario/', views.CreateUsuario, name='Novo_Usuario'),
    path('apaga_usuario/<int:pk>/', views.DeleteUsuario, name='Apaga_Usuario'),
    path('mostra_usuario/', views.MostraUsuario, name='Mostra_Usuario'),
    path('atualiza_usuario/<int:pk>', views.UpdateUsuario, name='Atualiza_Usuario'),
]
