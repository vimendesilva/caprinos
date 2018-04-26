from django.shortcuts import render, redirect
from . import forms
from .models import Cabra, Bode
# Create your views here.

def CreateCabra(request):

    if(request.method == 'POST'):
        form = forms.CreateCabras(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_cabras')

    else:
        form = forms.CreateCabras()

    return render(request, 'createCabra.html', {'cabra_form': form})


def CreateBode(request):

    if(request.method == 'POST'):
        form = forms.CreateBodes(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_bodes')

    else:
        form = forms.CreateBodes()
    
    return render(request, 'createBode.html', {'bode_form': form})


def CreateCobertura(request):

    if(request.method == 'POST'):
        form = forms.CreateCoberturas(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/nova_cobertura')

    else:
        form = forms.CreateCoberturas()

    return render(request, 'createCobertura.html', {'cobertura_form': form})


def MostraCabras(request):

    cabras = Cabra.objects.all()
    return render(request, 'mostraCabras.html', {'cabras': cabras})


def MostraBodes(request):

    bodes = Bode.objects.all()
    return render(request, 'mostraBodes.html', {'bodes': bodes})