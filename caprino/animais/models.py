from django.db import models


class Animal(models.Model):

    rgb_animal = models.CharField(verbose_name='RGD', max_length=50, blank=True, null=True)
    nome_animal = models.CharField(verbose_name='Nome', max_length=50, blank=True, null=True)
    numero_animal = models.IntegerField(verbose_name='Numero', blank=True, null=True)
    sexo_animal = models.CharField(verbose_name='Sexo', max_length=50)
    nascimento_animal = models.DateField(verbose_name='Nascimento', default=None)
    raca_animal = models.CharField(verbose_name='Raça', max_length=50)    
    sangue_animal = models.CharField(verbose_name='Sangue', max_length=50)
    brincos_animal = models.CharField(verbose_name='Brincos', max_length=50)
    vida_animal = models.CharField(verbose_name='Vida', blank=True, null=True, max_length=50)
    mae_animal = models.CharField(verbose_name='Mãe', max_length=50, blank=True, null=True)
    pai_animal = models.CharField(verbose_name='Pai', max_length=50, blank=True, null=True)
    foto_animal = models.ImageField(verbose_name='Foto', upload_to='img/' , blank=True, null=True)
    observacao_animal = models.TextField(verbose_name='Observação', blank=True, null=True)

    def __str__(self):
        return str(self.brincos_animal)

    class Meta:
        verbose_name = 'Animal'


class Cobertura(models.Model):
    inicio_cobertura = models.DateField(verbose_name='Início', blank=True, null=True, default=None)
    fim_cobertura = models.DateField(verbose_name='Fim', blank=True, null=True, default=None)
    id_bode = models.ForeignKey(Animal, verbose_name="Bode", related_name="Bode", on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = 'Cobertura'


class StatusCobertura(models.Model):
    status_cobertura = models.CharField(
        verbose_name='Início', blank=True, null=True, default=None, max_length=50)
    id_cabra = models.ForeignKey(
        Animal, verbose_name="Cabra", related_name="Cabra", on_delete=models.SET_NULL, null=True)
    id_cobertura = models.ForeignKey(Cobertura, verbose_name="Cobertura",
                                related_name="Cobertura", on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = 'StatusCobertura'


class Producao(models.Model):
    data_producao = models.DateField(verbose_name='Data')
    manha_producao = models.DecimalField(verbose_name='Peso Manhã', max_digits=5, decimal_places=4, blank=True, null=True)
    tarde_producao = models.DecimalField(verbose_name='Peso Tarde', max_digits=5, decimal_places=4, blank=True, null=True)
    descarte_producao = models.CharField(verbose_name='Descarte Produção', max_length=50, blank=True, null=True)
    id_cabra = models.ForeignKey(Animal, verbose_name="Cabra", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Producao'


class Parto(models.Model):
    data_parto = models.DateField(verbose_name='Data')
    parto = models.CharField(verbose_name='Tipo de Parto', max_length=50, blank=True, null=True)
    vivos_parto = models.IntegerField(verbose_name='Vivos', blank=True, null=True)
    observacao_parto = models.TextField(verbose_name='Observação', blank=True)
    id_cobertura = models.ForeignKey(Cobertura, verbose_name="Cobertura", on_delete=models.SET_NULL, null=True)
    id_cabra = models.ForeignKey(Animal, verbose_name="Animal", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Parto'


class Medicacao(models.Model):
    id_animal = models.ForeignKey(Animal, verbose_name="Animal", on_delete=models.SET_NULL, null=True)
    medicacao = models.CharField(verbose_name='Medicação', max_length=50, blank=True, null=True)
    data_medicacao = models.DateField(verbose_name='Data de Aplicação', default=None)
    observacao_medicacao = models.TextField(verbose_name='Observação', blank=True, null=True)
    inicio_carencia = models.DateField(verbose_name='Início', default=None, blank=True, null=True)
    fim_carencia = models.DateField(verbose_name='Fim', default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Medicacao'

class TipoMedicacao(models.Model):
    tipo_medicacao = models.CharField(verbose_name='Tipo Medicação', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'TipoMedicacao'

class Sangue(models.Model):
    sangue = models.CharField(verbose_name='Sangue', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Sangue'

class Raca(models.Model):
    raca = models.CharField(verbose_name='Raça', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Raca'

class TipoParto(models.Model):
    tipo_parto = models.CharField(verbose_name='Tipo Parto', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'TipoParto'

class Sexo(models.Model):
    sexo = models.CharField(verbose_name='Sexo', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Sexo'

class Vida(models.Model):
    vida = models.CharField(verbose_name='Vida', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Vida'