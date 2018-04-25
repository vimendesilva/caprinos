from django.db import models


class Fazenda(models.Model):
    nome_fazenda = models.CharField(verbose_name='Nome da Fazenda', max_length=100)

    def __str__(self):
        return self.nome_fazenda

    class Meta:
        verbose_name = 'Fazenda'


class Cabra(models.Model):
    rgd_cabra = models.CharField(verbose_name='RGD', max_length=50, blank=True)
    nome_cabra = models.CharField(verbose_name='Nome', max_length=50, blank=True)
    numero_cabra = models.IntegerField(verbose_name='Numero')
    nascimento_cabra = models.DateField(verbose_name='Nascimento', blank=True, null=True, default=None)
    raca_cabra = models.CharField(verbose_name='Raça', max_length=50)
    sangue_cabra = models.CharField(verbose_name='Sangue', max_length=50, blank=True)
    brincos_cabra = models.CharField(verbose_name='Brincos', max_length=50)
    chifres_cabra = models.BooleanField(verbose_name='Chifres', blank=True)
    observacao_cabra = models.TextField(verbose_name='Observação', blank=True)
    id_fazenda = models.ForeignKey(Fazenda, verbose_name="Fazenda", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.numero_cabra

    class Meta:
        verbose_name = 'Cabra'


class Bode(models.Model):
    nome_bode = models.CharField(verbose_name='Nome', max_length=50, blank=True)
    id_fazenda = models.ForeignKey(Fazenda, verbose_name="Fazenda", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome_bode

    class Meta:
        verbose_name = 'Bode'


class Cobertura(models.Model):
    data_cobertura = models.DateField(verbose_name='Data', blank=True, null=True, default=None)
    id_cabra = models.ForeignKey(Cabra, verbose_name="Cabra", on_delete=models.SET_NULL, null=True)
    id_bode = models.ForeignKey(Bode, verbose_name="Bode", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Cobertura'


class Producao(models.Model):
    data_producao = models.DateTimeField(verbose_name='Data')
    peso_producao = models.DecimalField(verbose_name='Peso', max_digits=5, decimal_places=4)
    id_cabra = models.ForeignKey(Cabra, verbose_name="Cabra", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Producao'


class Parto(models.Model):
    data_parto = models.DateField(verbose_name='Data')
    observacao_parto = models.TextField(verbose_name='Observação', blank=True)
    id_cobertura = models.ForeignKey(Cobertura, verbose_name="Cobertura", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Parto'


class Filhote(models.Model):
    numero_filhote = models.IntegerField(verbose_name='Numero')
    peso_filhote = models.DecimalField(verbose_name='Peso', max_digits=5, decimal_places=4)
    sexo_filhote = models.CharField(verbose_name='Sexo', max_length=50, blank=True)
    reposicao_filhote = models.BooleanField(verbose_name='Reposição', blank=True)
    id_parto = models.ForeignKey(Parto, verbose_name="Parto", on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.numero_filhote


    class Meta:
        verbose_name = 'Filhote'


class Filiacao(models.Model):
    class Meta:
        verbose_name = 'Filiacao'


class Vacina(models.Model):
    class Meta:
        verbose_name = 'Vacina'


class Medicacao(models.Model):
    class Meta:
        verbose_name = 'Medicacao'
