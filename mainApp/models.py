from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Especie(models.Model):
    nome = models.CharField("Espécie de semente", max_length=50)
    class Meta:
        verbose_name = "espécie"

    def __str__(self):
        return str(self.nome)

class Variedade(models.Model):
    nome = models.CharField("Variedade de semente", max_length=50)
    tempIdeal = models.DecimalField("Temperatura ideal de armazenamento", max_digits=5, decimal_places=2)
    umidadeIdeal = models.DecimalField("Umidade ideal de armazenamento", max_digits=5, decimal_places=2)
    validade = models.DurationField("Tempo máximo de armazenamento")
    caracteristicas = models.CharField("Características gerais da variedade", max_length=50, blank=True)
    ciclo = models.DurationField()
    imagem = models.ImageField(upload_to='variedades', null=True, blank=True)
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nome)

class Guardiao(models.Model):
    identificador = models.CharField("CPF ou CNPJ", max_length=14, unique=True)
    nome = models.CharField("Nome completo", max_length=100)
    telefone = models.CharField(max_length=11, blank=True)
    class Meta:
        verbose_name = "guardião"
        verbose_name_plural = "gurdiões"
    
    def __str__(self):
        return str(self.nome)

class Endereco(models.Model):
    cep = models.CharField(max_length=8, null=True, blank=True)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    comunidade = models.CharField(max_length=100)
    municipio = models.CharField("município", max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    guardiao = models.ForeignKey(Guardiao, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "endereço"

class Registro(models.Model):
    dataEntrada = models.DateTimeField('Data de entrada', default=timezone.now)
    safra = models.DateField('Data de colheita das sementes')
    observacoes = models.CharField('Observações gerais', max_length=300)
    guardiao = models.ForeignKey(Guardiao, on_delete=models.CASCADE)
    variedade = models.ForeignKey(Variedade, on_delete=models.CASCADE)
    class Meta:
        ordering = ['dataEntrada']

    def __str__(self):
        return f"{self.variedade} {self.guardiao} {self.dataEntrada}"

class Armario(models.Model):
    nome = models.CharField(max_length=30)
    class Meta:
        verbose_name = "armário"

    def __str__(self):
        return str(self.nome)

class Sensor(models.Model):
    nome = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "sensores"

    def __str__(self):
        return str(self.nome)
class Posicao(models.Model): # Utilizar os campos prateleira, armario como chave primaria juntos
    prateleira = models.CharField(max_length=30)
    armario = models.ForeignKey(Armario, on_delete=models.CASCADE)
    sensores = models.ManyToManyField(Sensor) # Verificar o comportamento do on_delete=CASCADE em many to many
    class Meta:
        verbose_name = "posição"
        verbose_name_plural = "posições"

    def __str__(self):
        return f"{self.prateleira} {self.armario}"

class Unidade(models.Model):
    nome = models.CharField(max_length=30)
    sigla = models.CharField(max_length=10)

    def __str__(self):
        return str(self.nome)
class Recipiente(models.Model):
    qrCode = models.CharField(max_length=300, blank=True)
    quantidade = models.DecimalField(max_digits=7, decimal_places=2)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    posicao = models.ForeignKey(Posicao, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.qrCode)

class Saida(models.Model):
    data = models.DateTimeField('Data da saída', default=timezone.now)
    descricao = models.CharField('Justificativa da saída', max_length=300)
    recipiente = models.ForeignKey(Recipiente, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "saída"

class TipoTeste(models.Model):
    nome = models.CharField('Nome do tipo de teste', max_length=50)
    descricao = models.CharField('Descrição do tipo de teste', max_length=300)
    class Meta:
        verbose_name = "tipo de teste"
        verbose_name_plural = "tipos de teste"

    def __str__(self):
        return str(self.nome)

class Teste(models.Model):
    resultado = models.CharField('Resultado do teste', max_length=50)
    data = models.DateTimeField('Data de realização do teste', default=timezone.now)
    observacoes = models.CharField('Observações gerais sobre o teste', max_length=300, blank=True)
    local = models.CharField('Local de realização do teste', max_length=50)
    imagem = models.ImageField(upload_to='testes', null=True, blank=True)
    tipoTeste = models.ForeignKey(TipoTeste, on_delete=models.PROTECT)
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT)