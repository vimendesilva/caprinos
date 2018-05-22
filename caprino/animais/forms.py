from django import forms
from . import models

class CreateAnimais(forms.ModelForm):
    SEXO = (('f', 'Feminino'), ('m', 'Masculino'))

    CHIFRE = (('1', 'Sim'), ('0', 'Não'))

    VIDA = (('1', 'Sim'), ('0', 'Não'))

    RACAS = (
        ('saanen', 'Saanen'),
        ('anglo-nubiana', 'Anglo-Nubiana'),
        ('srd', 'Sem Raça Definida (SRD)')
    )

    SANGUE = (
        ('po', 'Puro de Origem'),
        ('pc', 'Puro de Cruza'),
        ('1/2', '1/2 Sangue'),
        ('3/4', '3/4 Sangue'),
        ('7/8', '7/8 Sangue'),
        ('15/16', '15/16 Sangue'),
        ('31/32', '31/32 Sangue'),
    )
    rgb_animal = forms.CharField(label='RGB', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RGB do Animal'}))
    nome_animal = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Animal'}))
    numero_animal = forms.IntegerField(required=True, label='Numero', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do Animal'}))
    sexo_animal = forms.ChoiceField(required=True, label='Sexo', widget=forms.Select(attrs={'class': 'form-control'}), choices=SEXO)
    nascimento_animal = forms.DateField(label='Nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Nascimento do Animal', 'type': 'date'}))
    raca_animal = forms.ChoiceField(required=True, label='Raça', widget=forms.Select(attrs={'class': 'form-control'}), choices=RACAS)
    sangue_animal = forms.ChoiceField(label='Sangue', widget=forms.Select(attrs={'class': 'form-control'}), choices=SANGUE)
    brincos_animal = forms.CharField(label='Brincos', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brincos'}))
    chifres_animal = forms.ChoiceField(label='Chifres', widget=forms.Select(attrs={'class': 'form-control'}), choices=CHIFRE)
    vida_animal = forms.ChoiceField(label='Vida', widget=forms.Select(attrs={'class': 'form-control'}), choices=VIDA)
    observacao_animal = forms.CharField(label='Observação', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observação'}))
    id_fazenda = forms.ModelChoiceField(label='Fazenda', queryset=models.Fazenda.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class':'form-control'}))

    class Meta():
        model = models.Animal 
        fields = '__all__'


class CreateCoberturas(forms.ModelForm):

    inicio_cobertura = forms.DateField(label='Inicio', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Início de Cobertura', 'type': 'date'}))
    fim_cobertura = forms.DateField(label='Fim', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fim de Cobertura', 'type': 'date'}))
    id_cabra = forms.ModelMultipleChoiceField(label='Cabra', required=False, queryset=models.Animal.objects.all(
    ), to_field_name='id', widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control'}))
    id_bode = forms.ModelChoiceField(label='Bode', queryset=models.Animal.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        model = models.Cobertura
        fields = '__all__'

    def save(self):
        data = self.cleaned_data
        cobertura = models.Cobertura(
            id_bode=data['id_bode'], inicio_cobertura=data['inicio_cobertura'], fim_cobertura=data['fim_cobertura'])
        cobertura.save()

        self.save_related_objects(cobertura)

    def save_related_objects(self, cobertura):
        cabras = self.cleaned_data.pop('id_cabra', {})

        for cabra in cabras:
            status_cobertura = models.StatusCobertura(
                id_cobertura=cobertura, id_cabra=cabra)
            status_cobertura.save()
        


class CreateProducao(forms.ModelForm):

    data_producao = forms.DateField(label='Data', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Produção', 'type': 'date'}))
    peso_producao = forms.CharField(label='Peso', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Peso Produção'}))
    id_cabra = forms.ModelChoiceField(label='Cabra', queryset=models.Animal.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
   

    class Meta():
        model = models.Producao
        fields = '__all__'
