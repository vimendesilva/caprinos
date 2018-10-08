from django.urls import path
from . import views

app_name = 'caprino.relatorios'

urlpatterns = [    
    
    path('relatorios_med/pdf', views.gerar_pdf_medicacoes, name='RelatoriosMedicacaoPDF'),
    path('relatorios_cob/pdf', views.gerar_pdf_coberturas, name='RelatoriosCoberturaPDF'),
    path('relatorios_par/pdf', views.gerar_pdf_partos, name='RelatoriosPartoPDF'),
    path('relatorios_prod/pdf', views.gerar_pdf_producoes, name='RelatoriosProducaoPDF'),
    path('relatorios_desc/pdf', views.gerar_pdf_descartes, name='RelatoriosDescartePDF'),

    path('categorias/', views.Categorias, name='Categorias'),
    path('relatorios_med/', views.RelatoriosMedicacao, name='RelatoriosMedicacao'),
    path('relatorios_cob/', views.RelatoriosCobertura, name='RelatoriosCobertura'),
    path('relatorios_part/', views.RelatoriosParto, name='RelatoriosParto'),
    path('relatorios_prod/', views.RelatoriosProducao, name='RelatoriosProducao'),
    path('relatorios_desc/', views.RelatoriosDescarte, name='RelatoriosDescarte'),
]