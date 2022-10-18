from enum import unique
from tabnanny import verbose
from typing_extensions import Required
from unittest.util import _MAX_LENGTH
from django.db import models

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(required=True, max_length=100)
    bairro = models.CharField(max_length=100)
    comunidade = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=3, decimal_places=7)
    latitude = models.DecimalField(max_digits=3, decimal_places=7)

class Guardiao:
    identificador = models.CharField("CPF ou CNPJ", max_length=14, required=True, unique=True)
    nome = models.CharField(required=True, max_length=100)
    telefone = models.CharField(required=True, max_length=11)

class Registro(models.Model):
    data_entrada = models.DateTimeField('Data de entrada', Required=True, default=DateTime.now())
    safra = models.DateField('Data de colheita das sementes', Required=True)
    observacoes = models.CharField('Observações gerais', max_length=300)

    class Meta:
        ordering = ['dataEntrada']


