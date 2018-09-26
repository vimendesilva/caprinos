from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from . import forms

def Entrar(request):
    if(request.method == 'POST'):
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = authenticate(request, username=usuario, password=senha)
        if(user is not None):
            login(request, user)

            return redirect('/')

        else:
            return redirect('/contas/entrar')

    return render(request, 'usuario/login.html')

def Sair(request):
    logout(request)
    return redirect('/contas/entrar')

def CreateUsuario(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = forms.CreateUsuario(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso!')
                return redirect('/contas/mostra_usuario')
        else:
            form = forms.CreateUsuario()

        data = {
            'usuario_form': form
        }

        return render(request, 'usuario/createUsuario.html', data)
    else:
        return redirect('/')

def UpdateUsuario(request, pk):

    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = forms.UpdateUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
            return redirect('/contas/mostra_usuario')
    else:
        form = forms.UpdateUsuario(instance=usuario)

    return render(request, 'usuario/updateUsuario.html', {'usuario_form': form, 'id': pk})

@login_required
def MostraUsuario(request):

    usuarios = User.objects.all()
    paginator = Paginator(usuarios, 5)

    page = request.GET.get('page')

    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)


    return render(request, 'usuario/mostraUsuarios.html', {'usuarios': usuarios})

@login_required
def DeleteUsuario(request, pk):

    usu = get_object_or_404(User, pk=pk)
    usu.delete()
    messages.add_message(request, messages.SUCCESS, 'Dados apagados com sucesso!')
    return redirect('/contas/mostra_usuario')