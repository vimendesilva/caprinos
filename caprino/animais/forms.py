from django import forms
from . import models

class CreateCabras(forms.ModelForm):

    rgd_cabra = forms.CharField(label='RGD', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RGD da Cabra'}))
    nome_cabra = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Cabra'}))
    numero_cabra = forms.IntegerField(required=True, label='Numero', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número da Cabra'}))
    nascimento_cabra = forms.DateField(label='Nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Nascimento da Cabra', 'type': 'date'}))
    raca_cabra = forms.CharField(required=True, label='Raça', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Raça da Cabra'}))
    sangue_cabra = forms.CharField(label='Sangue', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo Sanguíneo'}))
    brincos_cabra = forms.CharField(label='Brincos', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brincos'}))
    chifres_cabra = forms.BooleanField(label='Chifres', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chifres'}))
    observacao_cabra = forms.CharField(label='Observação', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observação'}))
    id_fazenda = forms.ModelChoiceField(label='Fazenda', queryset=models.Fazenda.objects.all(), empty_label='Selecione uma opção', to_field_name='nome_fazenda', widget=forms.Select(attrs={'class':'form-control'}))

    class Meta():
        model = models.Cabra 
        fields = '__all__'

class CreateBodes(forms.ModelForm):

    nome_bode = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Bode'}))
    id_fazenda = forms.ModelChoiceField(label='Fazenda', queryset=models.Fazenda.objects.all(), empty_label='Selecione uma opção', to_field_name='nome_fazenda', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        model = models.Bode
        fields = '__all__'

class CreateCoberturas(forms.ModelForm):

    data_cobertura = forms.DateField(label='Data', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Cobertura', 'type': 'date'}))
    id_cabra = forms.ModelChoiceField(label='Cabra', queryset=models.Cabra.objects.all(), empty_label='Selecione uma opção', to_field_name='nome_cabra', widget=forms.Select(attrs={'class': 'form-control'}))
    id_bode = forms.ModelChoiceField(label='Bode', queryset=models.Bode.objects.all(), empty_label='Selecione uma opção', to_field_name='nome_bode', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        model = models.Cobertura
        fields = '__all__'