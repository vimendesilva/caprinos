import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from weasyprint import HTML

from . import forms
from caprino.animais.models import *

@login_required
def RelatoriosProducao(request):

    if(request.method == 'POST'):
        cabra = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(cabra != '0'):
            producao = Producao.objects.raw("select * from animais_producao"+
                                " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                                " where animais_producao.id_cabra_id = "+cabra+
                                " and animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                                " order by animais_producao.data_producao desc;")
        else:
            producao = Producao.objects.raw("select * from animais_producao"+
                                " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                                " where animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                                " order by animais_producao.data_producao desc;")
        

        dia = [obj.data_producao.day for obj in producao]
        prod = [float(obj.manha_producao + obj.tarde_producao) for obj in producao]

        soma = sum(prod)
                
        grafico = {
            'data_prod': dia,
            'manha_prod': prod,
        }

        dados = {
            'grafico': json.dumps(grafico),
            'soma': soma,
            'producao': producao,
            'inicio': inicio,
            'fim': fim
        }

       
        return render(request, 'relatorios/relatorios.html', dados)

    else:
        cabras = Animal.objects.filter(sexo_animal=2).filter(vida_animal=2)

        return render(request, 'relatorios/relatorios_producao.html', {'cabras': cabras})


@login_required
def RelatoriosMedicacao(request):

    if(request.method == 'POST'):
        animal = request.POST.get('animal')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                        " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao_id"+
                                        " where animais_medicacao.id_animal_id="+animal+
                                        " and animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                        " order by animais_medicacao.id desc;")
            
        else:
            medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                        " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao_id"+
                                        " where animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                        " order by animais_medicacao.id desc;")

        return render(request, 'relatorios/medicacao.html', {'medicacoes': medicacoes})

    else:

        cabras = Animal.objects.filter(vida_animal=2)

        return render(request, 'relatorios/relatorios_medicacao.html', {'cabras': cabras})
    
@login_required
def RelatoriosCobertura(request):

    if(request.method == 'POST'):
        animal = request.POST.get('animal')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            coberturas = Cobertura.objects.raw(
                '''
                SELECT ac.id, 
                (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = sc.id_cabra_id) AS Cabra,
                (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = ac.id_bode_id) AS Bode,
                ac.inicio_cobertura, ac.fim_cobertura, sc.status_cobertura
                FROM animais_cobertura ac
                INNER JOIN animais_statuscobertura sc ON ac.id = sc.id_cobertura_id
                WHERE sc.id_cabra_id = ''' + animal + '''
                AND ac.inicio_cobertura BETWEEN "''' + inicio + '''" AND "''' + fim + '''"
                '''
            )
        
        else:
            coberturas = Cobertura.objects.raw(
                '''
                SELECT ac.id,
                (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = sc.id_cabra_id) AS Cabra,
                (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = ac.id_bode_id) AS Bode,
                ac.inicio_cobertura, ac.fim_cobertura, sc.status_cobertura
                FROM animais_cobertura ac
                INNER JOIN animais_statuscobertura sc ON ac.id = sc.id_cobertura_id
                WHERE ac.inicio_cobertura BETWEEN "''' + inicio + '''" AND "''' + fim + '''"
                '''
            )

        return render(request, 'relatorios/cobertura.html', {'coberturas': coberturas})

    else:

        cabras = Animal.objects.filter(sexo_animal=2).filter(vida_animal=2)

        return render(request, 'relatorios/relatorios_cobertura.html', {'cabras': cabras})

@login_required
def RelatoriosParto(request):

    if(request.method == 'POST'):
        animal = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            partos = Parto.objects.raw("select * from animais_parto"+
                                " inner join animais_animal on animais_parto.id_cabra_id = animais_animal.id"+
                                " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto_id"+
                                " where animais_parto.id_cabra_id = "+animal+
                                " and animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                                " order by animais_parto.id desc;")
        else:
            partos = Parto.objects.raw("select * from animais_parto"+
                                    " inner join animais_animal on animais_parto.id_cabra_id = animais_animal.id"+
                                    " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto_id"+
                                    " where animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                                    " order by animais_parto.id desc;")

        print(partos)
        return render(request, 'relatorios/parto.html', {'partos': partos})

    else:

        cabras = Animal.objects.filter(sexo_animal=2).filter(vida_animal=2)

        return render(request, 'relatorios/relatorios_parto.html', {'cabras': cabras})


@login_required
def RelatoriosDescarte(request):

    if(request.method == 'POST'):
        cabra = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(cabra != '0'):
            producao = Producao.objects.raw("select * from animais_producao"+
                                " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                                " where animais_producao.id_cabra_id = "+animal+
                                " and animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                                " and animais_producao.descarte_producao = 1"
                                " order by animais_producao.data_producao desc;")
        else:
            producao = Producao.objects.raw("select * from animais_producao"+
                                " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                                " where animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                                " and animais_producao.descarte_producao = 1"
                                " order by animais_producao.data_producao desc;")
        

        dia = [obj.data_producao.day for obj in producao]
        prod = [float(obj.manha_producao + obj.tarde_producao) for obj in producao]

        soma = sum(prod)
                
        grafico = {
            'data_prod': dia,
            'manha_prod': prod,
        }

        dados = {
            'grafico': json.dumps(grafico),
            'soma': soma,
            'producao': producao
        }

        return render(request, 'relatorios/descarte.html', dados)

    else:
        cabras = Animal.objects.filter(sexo_animal=2).filter(vida_animal=2)

        return render(request, 'relatorios/relatorios_descarte.html', {'cabras': cabras})


@login_required
def Categorias(request):

    return render(request, 'relatorios/categorias.html')


def gerar_pdf_medicacoes(request):
    
    animal = request.POST.get('animal')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')

    if(animal != '0'):
        medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                    " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao_id"+
                                    " where animais_medicacao.id_animal_id="+animal+
                                    " and animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                    " order by animais_medicacao.id desc;")
        
    else:
        medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                    " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao_id"+
                                    " where animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                    " order by animais_medicacao.id desc;")
    
    dados = {
        'medicacoes': medicacoes,
        'inicio': inicio,
        'fim': fim
    }
    html_string = render_to_string('relatorios/tabela_medicacao.html', dados)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/medicacoes.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('medicacoes.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="medicacoes.pdf"'
        return response

    return response


def gerar_pdf_coberturas(request):
    
    animal = request.POST.get('animal')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')
    print(inicio)

    if(animal != '0'):
        coberturas = Cobertura.objects.raw(
            '''
            SELECT ac.id,
            (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = sc.id_cabra_id) AS Cabra,
            (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = ac.id_bode_id) AS Bode,
            ac.inicio_cobertura, ac.fim_cobertura, sc.status_cobertura
            FROM animais_cobertura ac
            INNER JOIN animais_statuscobertura sc ON ac.id = sc.id_cobertura_id
            WHERE sc.id_cabra_id = ''' + animal + '''
            AND ac.inicio_cobertura BETWEEN "''' + inicio + '''" AND "''' + fim + '''"
            '''
        )
        
    else:
        coberturas = Cobertura.objects.raw(
            '''
            SELECT ac.id,
            (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = sc.id_cabra_id) AS Cabra,
            (SELECT aa.brincos_animal FROM animais_animal aa WHERE aa.id = ac.id_bode_id) AS Bode,
            ac.inicio_cobertura, ac.fim_cobertura, sc.status_cobertura
            FROM animais_cobertura ac
            INNER JOIN animais_statuscobertura sc ON ac.id = sc.id_cobertura_id
            WHERE ac.inicio_cobertura BETWEEN "''' + inicio + '''" AND "''' + fim + '''"
            '''
        )
        
    dados = {
        'coberturas': coberturas,
        'inicio': inicio,
        'fim': fim
    }
    html_string = render_to_string('relatorios/tabela_cobertura.html', dados)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/coberturas.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('coberturas.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="coberturas.pdf"'
        return response

    return response

def gerar_pdf_partos(request):
    
    animal = request.POST.get('cabra')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')

    if(animal != '0'):
        partos = Parto.objects.raw("select * from animais_parto"+
                            " inner join animais_animal on animais_parto.id_cabra_id = animais_animal.id"+
                            " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto_id"+
                            " where animais_parto.id_cabra_id = "+animal+
                            " and animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                            " order by animais_parto.id desc;")
    else:
        partos = Parto.objects.raw("select * from animais_parto"+
                " inner join animais_animal on animais_parto.id_cabra_id = animais_animal.id"+
                " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto_id"+
                " where animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                " order by animais_parto.id desc;")

    dados = {
        'partos': partos,
        'inicio': inicio,
        'fim': fim
    }
    html_string = render_to_string('relatorios/tabela_parto.html', dados)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/partos.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('partos.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="partos.pdf"'
        return response

    return response

def gerar_pdf_producoes(request):
    
    cabra = request.POST.get('cabra')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')

    if(cabra != '0'):
        producao = Producao.objects.raw("select * from animais_producao"+
                            " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                            " where animais_producao.id_cabra_id = "+animal+
                            " and animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                            " order by animais_producao.data_producao desc;")
    else:
        producao = Producao.objects.raw("select * from animais_producao"+
                            " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                            " where animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                            " order by animais_producao.data_producao desc;")
        

    dados = {
        'producao': producao,
        'inicio': inicio,
        'fim': fim
    }
    html_string = render_to_string('relatorios/tabela_producao.html', dados)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/producao.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('producao.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="producao.pdf"'
        return response

    return response

def gerar_pdf_descartes(request):
    
    cabra = request.POST.get('cabra')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')

    if(cabra != '0'):
        producao = Producao.objects.raw("select * from animais_producao"+
                            " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                            " where animais_producao.id_cabra_id = "+animal+
                            " and animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                            " and animais_producao.descarte_producao = 1"
                            " order by animais_producao.data_producao desc;")
    else:
        producao = Producao.objects.raw("select * from animais_producao"+
                            " inner join animais_animal on animais_producao.id_cabra_id = animais_animal.id"+
                            " where animais_producao.data_producao between '"+inicio+"' and '"+fim+"'"+
                            " and animais_producao.descarte_producao = 1"
                            " order by animais_producao.data_producao desc;")
        
    dados = {
        'producao': producao,
        'inicio': inicio,
        'fim': fim
    }
    html_string = render_to_string('relatorios/tabela_descarte.html', dados)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/descarte.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('descarte.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="descarte.pdf"'
        return response

    return response