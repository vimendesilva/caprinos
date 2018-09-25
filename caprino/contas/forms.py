from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User


class CreateUsuario(UserCreationForm):

    first_name = forms.CharField(label='Nome:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail:', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Nome de usuário:', widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': False}))
    password1 = forms.CharField(label='Senha:', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmação de Senha:', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    is_superuser = forms.BooleanField(label='Administrador', widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        data = self.cleaned_data

        usuario = User()

        usuario.first_name      = data['first_name']
        usuario.last_name       = data['last_name']
        usuario.email           = data['email']
        usuario.username        = data['username']
        usuario.is_staff        = data['is_superuser']
        usuario.is_superuser    = data['is_superuser']

        usuario.set_password(data['password1'])

        usuario.save()

        return usuario


class UpdateUsuario(forms.ModelForm):

    first_name = forms.CharField(label='Nome:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail:', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # username = forms.CharField(label='Nome de usuário:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password1 = forms.CharField(label='Senha:', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # password2 = forms.CharField(label='Confirmação de Senha:', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    is_superuser = forms.BooleanField(label='Administrador', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_superuser')
