from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
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

    return render(request, 'login.html')


def Sair(request):
    logout(request)
    return redirect('/contas/entrar')


