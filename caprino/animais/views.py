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
from .models import Animal, Cobertura, Producao, StatusCobertura, Medicacao, Parto


@login_required
def CreateAnimal(request):

    if(request.method == 'POST'):
        form = forms.CreateAnimais(request.POST, request.FILES)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
            return redirect('/animais/mostra_animal')

    else:
        form = forms.CreateAnimais()

    return render(request, 'createAnimais.html', {'animais_form': form})


@login_required
def CreateCobertura(request):

    if(request.method == 'POST'):

        form = forms.CreateCoberturas(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
            return redirect('/animais/mostra_coberturas')

    else:
        form = forms.CreateCoberturas()

    return render(request, 'createCobertura.html', {'cobertura_form': form})


@login_required
def CreateProducoes(request, pk):

    if(request.method == 'POST'):
        form = forms.CreateProducao(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
            return redirect('/animais/lista_cabras')

    else:
        form = forms.CreateProducao()
        cabra = Animal.objects.get(pk=pk)

    return render(request, 'createProducao.html', {'producao_form': form, 'cabra': cabra})

@login_required
def CreateMedicacao(request):

    if(request.method == 'POST'):
        form = forms.CreateMedicacao(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
            return redirect('/animais/mostra_medicacoes')

    else:
        form = forms.CreateMedicacao()

    return render(request, 'createMedicacao.html', {'medicacao_form': form})

@login_required
def CreateParto(request, pk):

    if(request.method == 'POST'):
        form = forms.CreateParto(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
            return redirect('/animais/coberturas_partos')

    else:
        cabras = Animal.objects.raw('select * from animais_animal'+ 
                                            ' inner join animais_statuscobertura on animais_animal.id = animais_statuscobertura.id_cabra_id'+
                                            ' inner join animais_cobertura on animais_statuscobertura.id_cobertura_id = animais_cobertura.id'+
                                            ' where animais_cobertura.id = '+ str(pk) +' and animais_statuscobertura.status_cobertura = "1"')
        form = forms.CreateParto()

    return render(request, 'createParto.html', {'parto_form': form, 'id_cob': pk, 'cabras': cabras})


@login_required
def ListaCabras(request):

    animais = Animal.objects.all()
    paginator = Paginator(animais, 5)

    page = request.GET.get('page')

    try:
        animais = paginator.page(page)
    except PageNotAnInteger:
        animais = paginator.page(1)
    except EmptyPage:
        animais = paginator.page(paginator.num_pages)

    return render(request, 'listaCabras.html', {'animais': animais})


@login_required
def MostraAnimal(request):

    animais = Animal.objects.all()
    paginator = Paginator(animais, 5)

    page = request.GET.get('page')

    try:
        animais = paginator.page(page)
    except PageNotAnInteger:
        animais = paginator.page(1)
    except EmptyPage:
        animais = paginator.page(paginator.num_pages)


    return render(request, 'mostraAnimais.html', {'animais': animais})


@login_required
def MostraCoberturas(request):

    coberturas = Cobertura.objects.all().order_by('-id')
    paginator = Paginator(coberturas, 5)

    page = request.GET.get('page')

    try:
        coberturas = paginator.page(page)
    except PageNotAnInteger:
        coberturas = paginator.page(1)
    except EmptyPage:
        coberturas = paginator.page(paginator.num_pages)

    return render(request, 'mostraCoberturas.html', {'coberturas': coberturas})


@login_required
def MostraProducao(request, pk):

    producao = Producao.objects.all().filter(id_cabra_id=pk).order_by('-data_producao')
    paginator = Paginator(producao, 30)

    page = request.GET.get('page')

    try:
        producao = paginator.page(page)
    except PageNotAnInteger:
        producao = paginator.page(1)
    except EmptyPage:
        producao = paginator.page(paginator.num_pages)

    return render(request, 'mostraProducao.html', {'producao': producao, 'cabra': pk})

@login_required
def MostraMedicacoes(request):

    medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                        " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao"+
                                        " order by animais_medicacao.id desc;")
    paginator = Paginator(medicacoes, 5)
    
    page = request.GET.get('page')

    try:
        medicacoes = paginator.page(page)
    except PageNotAnInteger:
        medicacoes = paginator.page(1)
    except EmptyPage:
        medicacoes = paginator.page(paginator.num_pages)

    return render(request, 'mostraMedicacoes.html', {'medicacoes': medicacoes})

@login_required
def MostraParto(request, pk):

    parto = Parto.objects.raw("select * from animais_parto"+
                                " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto"+
                                " where animais_parto.id_cobertura_id="+str(pk)+
                                " order by animais_parto.id desc;")

    paginator = Paginator(parto, 30)

    page = request.GET.get('page')

    try:
        parto = paginator.page(page)
    except PageNotAnInteger:
        parto = paginator.page(1)
    except EmptyPage:
        parto = paginator.page(paginator.num_pages)

    return render(request, 'mostraParto.html', {'parto': parto, 'id_cobertura': pk})


@login_required
def DeleteAnimal(request, pk):

    cabra = get_object_or_404(Animal, pk=pk)
    cabra.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/animais/mostra_animal')


@login_required
def DeleteCobertura(request, pk):

    cobertura = get_object_or_404(Cobertura, pk=pk)
    cobertura.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/animais/mostra_coberturas')


@login_required
def DeleteProducao(request, pk):
    producao = get_object_or_404(Producao, pk=pk)
    producao.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/animais/lista_cabras')

@login_required
def DeleteMedicacao(request, pk):
    medicacao = get_object_or_404(Medicacao, pk=pk)
    medicacao.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/animais/mostra_medicacoes')
    
@login_required
def DeleteParto(request, pk):
    parto = get_object_or_404(Parto, pk=pk)
    parto.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/animais/coberturas_partos')

@login_required
def UpdateAnimal(request, pk):

    cabra = get_object_or_404(Animal, pk=pk)

    if(request.method == 'POST'):
        form = forms.CreateAnimais(request.POST, request.FILES, instance=cabra)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/animais/mostra_animal')

    else:
        form = forms.CreateAnimais(instance=cabra)

    return render(request, 'updateAnimais.html', {'animais_form': form})


@login_required
def UpdateCobertura(request, pk):

    cobertura = get_object_or_404(Cobertura, pk=pk)
    cabras = StatusCobertura.objects.filter(id_cobertura=pk)

    if(request.method == 'POST'):
        form = forms.CreateCoberturas(request.POST, instance=cobertura)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/animais/mostra_coberturas')

    else:
        form = forms.CreateCoberturas(instance=cobertura)

    return render(request, 'updateCobertura.html', {'cobertura_form': form, 'cabras': cabras, 'cob': pk})


@login_required
def UpdateProducao(request, id_prod, id_cabra):

    producao = get_object_or_404(Producao, pk=id_prod)
    if(request.method == 'POST'):
        form = forms.CreateProducao(request.POST, instance=producao)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/animais/lista_cabras')

    else:
        form = forms.CreateProducao(instance=producao)
        cabra = Animal.objects.get(pk=id_cabra)

    return render(request, 'updateProducao.html', {'producao_form': form, 'cabra': cabra})

@login_required
def UpdateMedicacao(request, pk):

    medicacao = get_object_or_404(Medicacao, pk=pk)

    if(request.method == 'POST'):
        form = forms.CreateMedicacao(request.POST, instance=medicacao)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/animais/mostra_medicacoes')

    else:
        form = forms.CreateMedicacao(instance=medicacao)

    return render(request, 'updateMedicacao.html', {'medicacao_form': form})

@login_required
def UpdateParto(request, id_parto, id_cob):

    parto = get_object_or_404(Parto, pk=id_parto)
    if(request.method == 'POST'):
        form = forms.CreateParto(request.POST, instance=parto)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/animais/coberturas_partos')

    else:
        form = forms.CreateParto(instance=parto)
        cobertura = Cobertura.objects.get(pk=id_cob)
        cabras = Animal.objects.raw('select * from animais_animal'+ 
                                            ' inner join animais_statuscobertura on animais_animal.id = animais_statuscobertura.id_cabra_id'+
                                            ' inner join animais_cobertura on animais_statuscobertura.id_cobertura_id = animais_cobertura.id'+
                                            ' where animais_cobertura.id = '+ str(id_cob) +' and animais_statuscobertura.status_cobertura = "1"')

    return render(request, 'updateParto.html', {'parto_form': form, 'id_cob': cobertura, 'cabras': cabras})

@login_required
def CoberturasPartos(request):

    coberturas = Cobertura.objects.all().order_by('-id')
    paginator = Paginator(coberturas, 5)

    page = request.GET.get('page')

    try:
        coberturas = paginator.page(page)
    except PageNotAnInteger:
        coberturas = paginator.page(1)
    except EmptyPage:
        coberturas = paginator.page(paginator.num_pages)

    return render(request, 'coberturas_partos.html', {'coberturas': coberturas})


@login_required
def RelatoriosProducao(request):

    if(request.method == 'POST'):
        cabra = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(cabra != '0'):
            producao = Producao.objects.filter(id_cabra_id=cabra).filter(data_producao__range=(inicio, fim))
        else:
            producao = Producao.objects.filter(data_producao__range=(inicio, fim))
        

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

        return render(request, 'relatorios.html', dados)

    else:
        cabras = Animal.objects.filter(sexo_animal='f').filter(vida_animal='s')

        return render(request, 'relatorios_producao.html', {'cabras': cabras})


@login_required
def RelatoriosMedicacao(request):

    if(request.method == 'POST'):
        animal = request.POST.get('animal')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                        " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao"+
                                        " where animais_medicacao.id_animal_id="+animal+
                                        " and animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                        " order by animais_medicacao.id desc;")
            
        else:
            medicacoes = Medicacao.objects.raw("select * from animais_medicacao"+
                                        " inner join animais_tipomedicacao on animais_tipomedicacao.id = animais_medicacao.medicacao"+
                                        " where animais_medicacao.data_medicacao between '"+inicio+"' and '"+fim+"'"
                                        " order by animais_medicacao.id desc;")

        return render(request, 'medicacao.html', {'medicacoes': medicacoes})

    else:

        cabras = Animal.objects.filter(sexo_animal='f').filter(vida_animal='s')

        return render(request, 'relatorios_medicacao.html', {'cabras': cabras})
    
@login_required
def RelatoriosCobertura(request):

    if(request.method == 'POST'):
        animal = request.POST.get('animal')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            coberturas = Cobertura.objects.raw('select * from animais_cobertura '+
                                            'inner join animais_statuscobertura on animais_cobertura.id = animais_statuscobertura.id_cobertura_id '+
                                            'where animais_statuscobertura.id_cabra_id = '+animal+
                                            ' and (animais_cobertura.inicio_cobertura >= "'+inicio+ '" and animais_cobertura.fim_cobertura <= "'+fim+ '");')
            
        else:
            coberturas = Cobertura.objects.raw('select * from animais_cobertura '+
                                            'inner join animais_statuscobertura on animais_cobertura.id = animais_statuscobertura.id_cobertura_id '+
                                            'where animais_cobertura.inicio_cobertura >= "'+inicio+ '" and animais_cobertura.fim_cobertura <= "'+fim+ '";')

        return render(request, 'cobertura.html', {'coberturas': coberturas})

    else:

        cabras = Animal.objects.filter(sexo_animal='f').filter(vida_animal='s')

        return render(request, 'relatorios_cobertura.html', {'cabras': cabras})

@login_required
def RelatoriosParto(request):

    if(request.method == 'POST'):
        animal = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(animal != '0'):
            partos = Parto.objects.raw("select * from animais_parto"+
                                " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto"+
                                " where animais_parto.id_cabra_id = "+animal+
                                " and animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                                " order by animais_parto.id desc;")
        else:
            partos = Parto.objects.raw("select * from animais_parto"+
                    " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto"+
                    " where animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                    " order by animais_parto.id desc;")

        print(partos)
        return render(request, 'parto.html', {'partos': partos})

    else:

        cabras = Animal.objects.filter(sexo_animal='f').filter(vida_animal='s')

        return render(request, 'relatorios_parto.html', {'cabras': cabras})


@login_required
def RelatoriosDescarte(request):

    if(request.method == 'POST'):
        cabra = request.POST.get('cabra')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')

        if(cabra != '0'):
            producao = Producao.objects.filter(id_cabra_id=cabra).filter(data_producao__range=(inicio, fim)).filter(descarte_producao='1')
        else:
            producao = Producao.objects.filter(data_producao__range=(inicio, fim)).filter(descarte_producao='1')
        

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

        return render(request, 'descarte.html', dados)

    else:
        cabras = Animal.objects.filter(sexo_animal='f').filter(vida_animal='s')

        return render(request, 'relatorios_descarte.html', {'cabras': cabras})


@login_required
def Categorias(request):

    return render(request, 'categorias.html')

@login_required
def SetStatusCobertura(request, id_cab, valor, id_cob):

    StatusCobertura.objects.filter(id_cobertura=id_cob).filter(id_cabra=id_cab).update(status_cobertura=valor)

    return redirect('/animais/atualiza_cobertura/{}'.format(id_cob))


@login_required
def VerificaPeriodoCarencia(request, id_cabra, data_producao):

    query = 'SELECT id FROM animais_medicacao WHERE id_animal_id = ' + str(id_cabra) + ' AND "' + data_producao + '" BETWEEN inicio_carencia AND fim_carencia;'

    try:
        resposta = Medicacao.objects.raw(query)[0]

        response = {
            'ok': False,
            'msg': 'Animal no período de carência' 
        }
    except:
        response = {
            'ok': True
        }
    
    return JsonResponse(response)


def gerar_pdf_medicacoes(request):
    
    animal = request.POST.get('animal')
    inicio = request.POST.get('inicio')
    fim = request.POST.get('fim')

    if(animal != '0'):
        medicacoes = Medicacao.objects.filter(id_animal_id=animal).filter(data_medicacao__range=(inicio, fim))
    else:
        medicacoes = Medicacao.objects.filter(data_medicacao__range=(inicio, fim))
        
    html_string = render_to_string('tabela_medicacao.html', {'medicacoes': medicacoes})

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

    if(animal != '0'):
        coberturas = Cobertura.objects.raw('select * from animais_cobertura '+
                                        'inner join animais_statuscobertura on animais_cobertura.id = animais_statuscobertura.id_cobertura_id '+
                                        'where animais_statuscobertura.id_cabra_id = '+animal+
                                        ' and (animais_cobertura.inicio_cobertura >= "'+inicio+ '" and animais_cobertura.fim_cobertura <= "'+fim+ '");')
        
    else:
        coberturas = Cobertura.objects.raw('select * from animais_cobertura '+
                                        'inner join animais_statuscobertura on animais_cobertura.id = animais_statuscobertura.id_cobertura_id '+
                                        'where animais_cobertura.inicio_cobertura >= "'+inicio+ '" and animais_cobertura.fim_cobertura <= "'+fim+ '";')

    html_string = render_to_string('tabela_cobertura.html', {'coberturas': coberturas})

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
                            " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto"+
                            " where animais_parto.id_cabra_id = "+animal+
                            " and animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                            " order by animais_parto.id desc;")
    else:
        partos = Parto.objects.raw("select * from animais_parto"+
                " inner join animais_tipoparto on animais_tipoparto.id = animais_parto.parto"+
                " where animais_parto.data_parto between '"+inicio+"' and '"+fim+"'"+
                " order by animais_parto.id desc;")

    html_string = render_to_string('tabela_parto.html', {'partos': partos})

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
        producao = Producao.objects.filter(id_cabra_id=cabra).filter(data_producao__range=(inicio, fim))
    else:
        producao = Producao.objects.filter(data_producao__range=(inicio, fim))
        

    html_string = render_to_string('tabela_producao.html', {'producao': producao})

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
        producao = Producao.objects.filter(id_cabra_id=cabra).filter(data_producao__range=(inicio, fim)).filter(descarte_producao='1')
    else:
        producao = Producao.objects.filter(data_producao__range=(inicio, fim)).filter(descarte_producao='1')
        

    html_string = render_to_string('tabela_descarte.html', {'producao': producao})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/descarte.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('descarte.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="descarte.pdf"'
        return response

    return response