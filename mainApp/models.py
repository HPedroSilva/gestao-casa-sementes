from enum import unique
from tabnanny import verbose
from tkinter import CASCADE
from typing_extensions import Required
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone

class Especie:
    nome = models.CharField("Espécie de semente", max_length=50)

class Variedade:
    nome = models.CharField("Variedade de semente", max_length=50)
    tempIdeal = models.DecimalField("Temperatura ideal de armazenamento", max_digits=3, decimal_places=2)
    umidadeIdeal = models.DecimalField("Umidade ideal de armazenamento", max_digits=3, decimal_places=2)
    validade = models.DurationField("Tempo máximo de armazenamento")
    caracteristicas = models.CharField("Características gerais da variedade", max_length=50)
    ciclo = models.DurationField()
    imagem = models.ImageField(upload_to='/variedades')
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)

class Guardiao:
    identificador = models.CharField("CPF ou CNPJ", max_length=14, required=True, unique=True)
    nome = models.CharField(required=True, max_length=100)
    telefone = models.CharField(required=True, max_length=11)

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(required=True, max_length=100)
    bairro = models.CharField(max_length=100)
    comunidade = models.CharField(max_length=100)
    municipio = models.CharField("município", max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=3, decimal_places=7)
    latitude = models.DecimalField(max_digits=3, decimal_places=7)
    guardiao = models.ForeignKey(Guardiao, on_delete=models.CASCADE)

class Registro(models.Model):
    data_entrada = models.DateTimeField('Data de entrada', Required=True, default=timezone.now())
    safra = models.DateField('Data de colheita das sementes', Required=True)
    observacoes = models.CharField('Observações gerais', max_length=300)
    guardiao = models.ForeignKey(Guardiao, on_delete=models.CASCADE)
    variedade = models.ForeignKey(Variedade, on_delete=models.CASCADE)

    class Meta:
        ordering = ['dataEntrada']

class Armario:
    nome = models.CharField(max_length=30, required=True)

class Sensor:
    nome = models.CharField(max_length=30, required=True)
class Posicao:
    prateleira = models.CharField(max_length=30, required=True)
    armario = models.ForeignKey(Armario, on_delete=CASCADE)
    sensores = models.ManyToManyField(Sensor, on_delete=CASCADE) # Verificar o comportamento do on_delete=CASCADE em many to many

class Unidade(models.Model):
    nome = models.CharField(max_length=30, required=True)
    sigla = models.CharField(max_length=10, requiered=True)

class Recipiente(models.Model):
    qrCode = models.CharField(max_length=300)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    posicao = models.ForeignKey(Posicao, on_delete=models.CASCADE)

class Saida(models.Model):
    data = models.DateTimeField('Data da saída', Required=True, default=timezone.now())
    descrição = models.CharField('Justificativa da saída', max_length=300)
    recipiente = models.ForeignKey(Recipiente, on_delete=models.CASCADE, required=True)