from django.urls import path
from . import views

app_name = 'caprino.animais'

urlpatterns = [

    path('novo_animal/', views.CreateAnimal, name='Novo_Animal'),
    path('apaga_animal/<int:pk>/', views.DeleteAnimal, name='Apaga_Animal'),
    path('mostra_animal/', views.MostraAnimal, name='Mostra_Animal'),
    path('atualiza_animal/<int:pk>', views.UpdateAnimal, name='Atualiza_Animal'),
    path('verifica_periodo_carencia/<int:id_cabra>/<str:data_producao>/', views.VerificaPeriodoCarencia, name='Verifica Periodo de Carencia'),

    path('nova_cobertura/', views.CreateCobertura, name='Nova_Cobertura'),
    path('mostra_coberturas/', views.MostraCoberturas, name='Mostra_Coberturas'),
    path('delete_cobertura/<int:pk>/', views.DeleteCobertura, name='Delete_Cobertura'),
    path('atualiza_cobertura/<int:pk>', views.UpdateCobertura, name='Atualiza_Cobertura'),

    path('lista_cabras/', views.ListaCabras, name='Lista_Cabras'),
    path('nova_producao/<int:pk>', views.CreateProducoes, name='Nova_Producao'),
    path('mostra_producao/<int:pk>', views.MostraProducao, name='Mostra_Producao'),
    path('delete_producao/<int:pk>', views.DeleteProducao, name='Delete_Producao'),
    path('atualiza_producao/<int:id_prod>/<int:id_cabra>', views.UpdateProducao, name='Atualiza_Producao'),

    path('nova_medicacao/', views.CreateMedicacao, name='Nova_Medicacao'),
    path('mostra_medicacoes/', views.MostraMedicacoes, name='Mostra_Medicacoes'),
    path('delete_medicacao/<int:pk>', views.DeleteMedicacao, name='Delete_Medicacao'),
    path('atualiza_medicacao/<int:pk>', views.UpdateMedicacao, name='Atualiza_Medicacao'),

    path('novo_parto/<int:pk>', views.CreateParto, name='Novo_Parto'),
    path('coberturas_partos/', views.CoberturasPartos, name='Coberturas_Partos'),
    path('mostra_partos/<int:pk>', views.MostraParto, name='Mostra_Parto'),
    path('delete_parto/<int:pk>', views.DeleteParto, name='Delete_Parto'),
    path('atualiza_parto/<int:id_parto>/<int:id_cob>', views.UpdateParto, name='Atualiza_Parto'),

    path('categorias/', views.Categorias, name='Categorias'),
    path('relatorios_med/', views.RelatoriosMedicacao, name='RelatoriosMedicacao'),
    path('relatorios_cob/', views.RelatoriosCobertura, name='RelatoriosCobertura'),
    path('relatorios_part/', views.RelatoriosParto, name='RelatoriosParto'),
    path('relatorios/', views.RelatoriosProducao, name='RelatoriosProducao'),
    path('relatorios_desc/', views.RelatoriosDescarte, name='RelatoriosDescarte'),

    path('status/<int:id_cab>/<int:valor>/<int:id_cob>', views.SetStatusCobertura, name='StatusCobertura'),

    path('relatorios_med/pdf', views.gerar_pdf_medicacoes, name='RelatoriosMedicacaoPDF'),
    path('relatorios_cob/pdf', views.gerar_pdf_coberturas, name='RelatoriosCoberturaPDF'),
    path('relatorios_par/pdf', views.gerar_pdf_partos, name='RelatoriosPartoPDF'),
    path('relatorios_prod/pdf', views.gerar_pdf_producoes, name='RelatoriosProducaoPDF'),
    path('relatorios_desc/pdf', views.gerar_pdf_descartes, name='RelatoriosDescartePDF'),
]
