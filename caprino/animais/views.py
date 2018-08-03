from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import forms
from .models import Animal, Cobertura, Producao, StatusCobertura
from django.contrib.auth.decorators import login_required

import datetime
import json

@login_required
def CreateAnimal(request):

    if(request.method == 'POST'):
        form = forms.CreateAnimais(request.POST)
        if(form.is_valid()):
            form.save()
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
            return redirect('/animais/lista_cabras')

    else:
        form = forms.CreateProducao()
        cabra = Animal.objects.get(pk=pk)

    return render(request, 'createProducao.html', {'producao_form': form, 'cabra': cabra})


@login_required
def ListaCabras(request):

    animais = Animal.objects.all()
    paginator = Paginator(animais, 2)

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
    paginator = Paginator(animais, 2)

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

    coberturas = Cobertura.objects.all()
    paginator = Paginator(coberturas, 2)

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

    producao = Producao.objects.all().filter(id_cabra_id=pk)
    paginator = Paginator(producao, 2)

    page = request.GET.get('page')

    try:
        producao = paginator.page(page)
    except PageNotAnInteger:
        producao = paginator.page(1)
    except EmptyPage:
        producao = paginator.page(paginator.num_pages)

    return render(request, 'mostraProducao.html', {'producao': producao, 'cabra': pk})


@login_required
def DeleteAnimal(request, pk):

    cabra = get_object_or_404(Animal, pk=pk)
    cabra.delete()
    return redirect('/animais/mostra_animal')


@login_required
def DeleteCobertura(request, pk):

    cobertura = get_object_or_404(Cobertura, pk=pk)
    cobertura.delete()
    return redirect('/animais/mostra_coberturas')


@login_required
def DeleteProducao(request, pk):
    producao = get_object_or_404(Producao, pk=pk)
    producao.delete()
    return redirect('/animais/lista_cabras')

@login_required
def UpdateAnimal(request, pk):

    cabra = get_object_or_404(Animal, pk=pk)
    print(cabra.chifres_animal)
    if(request.method == 'POST'):
        form = forms.CreateAnimais(request.POST, instance=cabra)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_animal')

    else:
        form = forms.CreateAnimais(instance=cabra)

    return render(request, 'updateAnimais.html', {'animais_form': form})


@login_required
def UpdateCobertura(request, pk):

    cobertura = get_object_or_404(Cobertura, pk=pk)
    cabras = StatusCobertura.objects.filter(id_cobertura=pk)

    print(cabras)

    if(request.method == 'POST'):
        form = forms.CreateCoberturas(request.POST, instance=cobertura)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_coberturas')

    else:
        form = forms.CreateCoberturas(instance=cobertura)

    return render(request, 'updateCobertura.html', {'cobertura_form': form, 'cabras': cabras})


@login_required
def UpdateProducao(request, pk):

    producao = get_object_or_404(Producao, pk=pk)
    print(producao.id_cabra)
    if(request.method == 'POST'):
        form = forms.CreateProducao(request.POST, instance=producao)
        if(form.is_valid()):
            print('oi querido')
            form.save()
            return redirect('/animais/lista_cabras')

    else:
        form = forms.CreateProducao(instance=producao)

    return render(request, 'updateProducao.html', {'producao_form': form})


@login_required
def Relatorios(request):

    # producao = Producao.objects.filter(id_cabra=pk)
    producao = Producao.objects.all()
    dia = [obj.data_producao.day for obj in producao]
    mes = [obj.data_producao.month for obj in producao]
    manha = [float(obj.manha_producao + obj.tarde_producao) for obj in producao]
    print(mes)

    lista = list(set(dia)) #tira valor repetido
    
    grafico = {
        'data_prod': lista,
        'manha_prod': manha,
    }

    dados = {
        'grafico': json.dumps(grafico)
    }

    ano = [obj.data_producao.year for obj in producao]    
    print(ano)

    return render(request, 'relatorios.html', dados)

    # CODIGO DO JONATHAN
    # queryset = Produto.objects.all()
    # nomes = [obj.nome for obj in producao]
    # precos = [float(obj.preco) for obj in producao]

    # SEPARA DIA DA DATA COMPLETA
    # data = producao[0].data_producao
    # print(data.day)

    # CODIGO DO JONATHAN
    # data = {
    #     'nomes': json.dumps(nomes),
    #     'precos': json.dumps(precos),
    # }

    # CODIGO DO JONATHAN
    # data = JSON.parse({{ producao|safe }});

@login_required
def SetStatusCobertura(request):

    StatusCobertura.objects.filter(id_cobertura=24).update(status_cobertura=1)

    return redirect('/animais/mostra_coberturas')
