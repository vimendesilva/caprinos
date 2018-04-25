from django.db import models

# Create your models here.
class Caprino(models.Model):

    nome = models.CharField(verbose_name='Nome Completo' ,max_length=50, blank=True, default=None)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Caprino'