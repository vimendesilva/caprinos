from django.urls import path
from . import views

app_name = 'caprino.contas'
urlpatterns = [
    path('entrar/', views.Entrar, name='Entrar'),
    path('sair/', views.Sair, name='Sair'),
]
