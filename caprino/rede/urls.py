from django.urls import path
from . import views

app_name = 'caprino.rede'

urlpatterns = [    
    
    path('rede/', views.MontaDados, name='MontaDados'),
    path('escolhe_rede/', views.EscolheRede, name='EscolheRede'),
]