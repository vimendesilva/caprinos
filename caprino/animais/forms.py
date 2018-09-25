from django import forms
from . import models

class CreateAnimais(forms.ModelForm):

    rgb_animal = forms.CharField(required=False, label='RGB', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RGB do Animal'}))
    nome_animal = forms.CharField(required=False, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Animal'}))
    numero_animal = forms.IntegerField(required=False, label='Numero', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do Animal'}))
    sexo_animal = forms.ModelChoiceField(required=True, label='Sexo', queryset=models.Sexo.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    nascimento_animal = forms.DateField(required=True, label='Nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Nascimento do Animal', 'type': 'date'}))
    raca_animal = forms.ModelChoiceField(required=True, label='Raça', queryset=models.Raca.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    sangue_animal = forms.ModelChoiceField(required=True, label='Sangue', queryset=models.Sangue.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    brincos_animal = forms.CharField(required=True, label='Brincos', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brincos'}))
    vida_animal = forms.ModelChoiceField(required=True, label='Vida', queryset=models.Vida.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    mae_animal = forms.ModelChoiceField(required=False, label='Mãe', queryset=models.Animal.objects.all().filter(sexo_animal='f').filter(vida_animal='s'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    pai_animal = forms.ModelChoiceField(required=False, label='Pai', queryset=models.Animal.objects.all().filter(sexo_animal='m').filter(vida_animal='s'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    observacao_animal = forms.CharField(required=False, label='Observação', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observação'}))
    foto_animal = forms.ImageField(required=False, label='Foto do animal')

    class Meta():
        model = models.Animal 
        fields = '__all__'


class CreateCoberturas(forms.ModelForm):

    inicio_cobertura = forms.DateField(required=True, label='Inicio', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Início de Cobertura', 'type': 'date'}))
    fim_cobertura = forms.DateField(required=True, label='Fim', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fim de Cobertura', 'type': 'date'}))
    id_cabra = forms.ModelMultipleChoiceField(required=True, label='Cabra', queryset=models.Animal.objects.all(
    ).filter(sexo_animal='f').filter(vida_animal='s'), to_field_name='id', widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control'}))
    id_bode = forms.ModelChoiceField(required=True, label='Bode', queryset=models.Animal.objects.all().filter(sexo_animal='m').filter(vida_animal='s'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

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

    data_producao = forms.DateField(required=True, label='Data', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Produção', 'type': 'date'}))
    manha_producao = forms.CharField(required=True, label='Peso Manhã', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Peso Manhã'}))
    tarde_producao = forms.CharField(required=True, label='Peso Tarde', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Peso Tarde'}))
          

    class Meta():
        model = models.Producao
        fields = ['data_producao', 'manha_producao', 'tarde_producao', 'id_cabra', 'descarte_producao']


class CreateMedicacao(forms.ModelForm):

    id_animal = forms.ModelChoiceField(required=True, label='Animal', queryset=models.Animal.objects.all().filter(vida_animal='s'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_medicacaao = forms.ModelChoiceField(required=True, label='Medicação', queryset=models.TipoMedicacao.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    data_medicacao = forms.DateField(required=True, label='Data de Aplicação', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Aplicação', 'type': 'date'}))
    observacao_medicacao = forms.CharField(required=False, label='Observação', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observação'}))
    inicio_carencia = forms.DateField(required=False, label='Início Carência', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Início Carência', 'type': 'date'}))
    fim_carencia = forms.DateField(required=False, label='Fim Carência', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fim Carência', 'type': 'date'}))

    class Meta():
        model = models.Medicacao  
        fields = '__all__'  

class CreateParto(forms.ModelForm):

    data_parto = forms.DateField(required=True, label='Data de Parto', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Parto', 'type': 'date'}))
    tipo_parto = forms.ModelChoiceField(required=True, label='Tipo', queryset=models.TipoParto.objects.all(), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))
    vivos_parto = forms.IntegerField(required=False, label='Vivos', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vivos'}))
    observacao_parto = forms.CharField(required=False, label='Observação', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observação'}))
    id_cabra = forms.ModelChoiceField(required=True, label='Animal', queryset=models.Animal.objects.all().filter(vida_animal='s').filter(sexo_animal='f'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        model = models.Parto  
        fields = '__all__' 

class Relatorio(forms.ModelForm):
    id_cabra = forms.ModelChoiceField(required=True, label='Animal', queryset=models.Animal.objects.all().filter(vida_animal='s').filter(sexo_animal='f'), empty_label='Selecione uma opção', to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        fields = '__all__'