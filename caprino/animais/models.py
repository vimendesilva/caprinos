from django.db import models


class Fazenda(models.Model):
    nome_fazenda = models.CharField(verbose_name='Nome da Fazenda', max_length=100)

    def __str__(self):
        return self.nome_fazenda

    class Meta:
        verbose_name = 'Fazenda'


class Animal(models.Model):

    rgb_animal = models.CharField(verbose_name='RGD', max_length=50, blank=True)
    nome_animal = models.CharField(verbose_name='Nome', max_length=50, blank=True)
    numero_animal = models.IntegerField(verbose_name='Numero')
    sexo_animal = models.CharField(verbose_name='Sexo', blank=True, max_length=50)
    nascimento_animal = models.DateField(verbose_name='Nascimento', blank=True, null=True, default=None)
    raca_animal = models.CharField(verbose_name='Raça', max_length=50)    
    sangue_animal = models.CharField(verbose_name='Sangue', max_length=50, blank=True)
    brincos_animal = models.CharField(verbose_name='Brincos', max_length=50)
    chifres_animal = models.CharField(
        verbose_name='Chifres', blank=True, max_length=50)
    vida_animal = models.CharField(
        verbose_name='Vida', blank=True, max_length=50)
    observacao_animal = models.TextField(verbose_name='Observação', blank=True)
    id_fazenda = models.ForeignKey(Fazenda, verbose_name="Fazenda", on_delete=models.SET_NULL, null=True)

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
    manha_producao = models.DecimalField(verbose_name='Peso Manhã', max_digits=5, decimal_places=4)
    tarde_producao = models.DecimalField(verbose_name='Peso Tarde', max_digits=5, decimal_places=4)
    id_cabra = models.ForeignKey(Animal, verbose_name="Cabra", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Producao'


class Parto(models.Model):
    data_parto = models.DateField(verbose_name='Data')
    observacao_parto = models.TextField(verbose_name='Observação', blank=True)
    id_cobertura = models.ForeignKey(Cobertura, verbose_name="Cobertura", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Parto'


class Filiacao(models.Model):
    class Meta:
        verbose_name = 'Filiacao'


class Vacina(models.Model):
    class Meta:
        verbose_name = 'Vacina'


class Medicacao(models.Model):
    class Meta:
        verbose_name = 'Medicacao'
