from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Cabra, Bode
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def CreateCabra(request):

    if(request.method == 'POST'):
        form = forms.CreateCabras(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_cabras')

    else:
        form = forms.CreateCabras()

    return render(request, 'createCabra.html', {'cabra_form': form})

@login_required
def CreateBode(request):

    if(request.method == 'POST'):
        form = forms.CreateBodes(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/mostra_bodes')

    else:
        form = forms.CreateBodes()
    
    return render(request, 'createBode.html', {'bode_form': form})

@login_required
def CreateCobertura(request):

    if(request.method == 'POST'):
        form = forms.CreateCoberturas(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/nova_cobertura')

    else:
        form = forms.CreateCoberturas()

    return render(request, 'createCobertura.html', {'cobertura_form': form})

@login_required
def MostraAnimais(request):

    cabras = Cabra.objects.all()
    bodes = Bode.objects.all()
    return render(request, 'mostraCabras.html', {'cabras': cabras, 'bodes': bodes})


def DeleteCabra(request, pk):

    cabra = get_object_or_404(Cabra, pk=pk)
    cabra.delete()
    return redirect('/animais/mostra_animais')
