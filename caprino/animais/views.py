from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Animal, Cobertura, Producao
from django.contrib.auth.decorators import login_required
# Create your views here.

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
def CreateProducoes(request):

    if(request.method == 'POST'):
        form = forms.CreateProducao(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_producao')

    else:
        form = forms.CreateProducao()

    return render(request, 'createProducao.html', {'producao_form': form})

@login_required
def MostraAnimal(request):

    animais = Animal.objects.all()
    return render(request, 'mostraAnimais.html', {'animais': animais})


@login_required
def MostraCoberturas(request):

    coberturas = Cobertura.objects.all()
    return render(request, 'mostraCoberturas.html', {'coberturas': coberturas})


@login_required
def MostraProducao(request):

    producao = Producao.objects.all()
    return render(request, 'mostraProducao.html', {'producao': producao})


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
    return redirect('/animais/mostra_producao')

@login_required
def UpdateAnimal(request, pk):

    cabra = get_object_or_404(Animal, pk=pk)
    
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

    if(request.method == 'POST'):
        form = forms.CreateCoberturas(request.POST, instance=cobertura)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_coberturas')

    else:
        form = forms.CreateCoberturas(instance=cobertura)

    return render(request, 'updateCobertura.html', {'cobertura_form': form})


@login_required
def UpdateProducao(request, pk):

    producao = get_object_or_404(Producao, pk=pk)

    if(request.method == 'POST'):
        form = forms.CreateProducao(request.POST, instance=producao)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_producao')

    else:
        form = forms.CreateProducao(instance=producao)

    return render(request, 'updateProducao.html', {'producao_form': form})
