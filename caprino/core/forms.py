from django import forms
from . import models

class Teste(forms.ModelForm):

    class Meta:
        model = models.Caprino
        fields = '__all__'
