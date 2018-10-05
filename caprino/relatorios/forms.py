from django import forms
from caprino.animais import models

class Relatorio(forms.ModelForm):
    id_cabra = forms.ModelChoiceField(required=True, label='Animal', queryset=models.Animal.objects.all().filter(vida_animal=2).filter(sexo_animal=2), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        fields = '__all__'