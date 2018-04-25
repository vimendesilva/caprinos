from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms

@login_required
def home(request):
	return render(request, 'dashboard.html', {'form': forms.Teste})
