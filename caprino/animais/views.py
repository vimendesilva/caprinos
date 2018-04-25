from django.shortcuts import render, redirect
from . import forms
# Create your views here.

def CreateCabra(request):

    if(request.method == 'POST'):
        form = forms.CreateCabras(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/nova_cabra')

    else:
        form = forms.CreateCabras()

    return render(request, 'createCabra.html', {'cabra_form': form})


def CreateBode(request):

    if(request.method == 'POST'):
        form = forms.CreateBodes(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/animais/novo_bode')

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
