from typing_extensions import Required
from unittest.util import _MAX_LENGTH
from django.db import models

class Registro(models.Model):
    descricao = models.CharField('Descrição', max_length=300)
    dataColheitaSemente = models.DateField('Data de colheita da semente', Required=True)
    dataEntrada = models.DateTimeField('Data de entrada', Required=True, default=DateTime.now())

    class Meta:
        ordering = ['dataEntrada']
        verbose_name = "registro"
        verbose_name_plural = "registros"


# Create your models here.
