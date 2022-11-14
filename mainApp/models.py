from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import qrcode
from django.core.files import File
from io import BytesIO
from PIL import Image

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagens')
    descricao = models.CharField('Descrição geral da imagem', max_length=300)
    registroEntrada = models.ForeignKey('RegistroEntrada', on_delete=models.CASCADE, null=True, blank=True)
    teste = models.ForeignKey('Teste', on_delete=models.CASCADE, null=True, blank=True)
    variedade = models.ForeignKey('Variedade', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "imagens"
    
    def __str__(self):
        return str(self.imagem)
class Especie(models.Model):
    nome = models.CharField("Espécie de semente", max_length=50)
    class Meta:
        verbose_name = "espécie"

    def __str__(self):
        return str(self.nome)

class Variedade(models.Model):
    nome = models.CharField("Variedade de semente", max_length=50)
    tempIdeal = models.DecimalField("Temperatura ideal de armazenamento", help_text="Temperatura em °C" , max_digits=5, decimal_places=2)
    umidadeIdeal = models.DecimalField("Umidade ideal de armazenamento", help_text="Umidade relativa do ambiente em %", max_digits=5, decimal_places=2)
    validade = models.PositiveIntegerField("Tempo máximo de armazenamento (validade)", help_text="Quantidade de DIAS que essa variedade pode ser armazenada até o plantio")
    caracteristicas = models.TextField("Características gerais da variedade", max_length=500, blank=True, help_text="Ficha técnica da variedade, descrevendo variados aspectos relacionados, como solos favorávies, irrigação, região, clima favorável, etc.")
    ciclo = models.PositiveIntegerField(help_text="Quantidade de DIAS do ciclo da variedade")
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, verbose_name="espécie")

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
    
    def __str__(self):
        return f"{self.logradouro} {self.bairro}, {self.municipio} - {self.estado}"

class RegistroEntrada(models.Model):
    data = models.DateTimeField('Data de entrada', default=timezone.now)
    safra = models.DateField('Data de colheita das sementes')
    descricao = models.CharField('Observações gerais', max_length=300)
    guardiao = models.ForeignKey(Guardiao, on_delete=models.PROTECT)
    variedade = models.ForeignKey(Variedade, on_delete=models.PROTECT)
    enderecoGuardiao = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    class Meta:
        ordering = ['data']

    def __str__(self):
        return f"{self.variedade} {self.guardiao} {self.data}"
    
    @property
    def dataValidade(self):
        validade = timedelta(days=self.variedade.validade)
        return validade + self.data
class Armario(models.Model):
    nome = models.CharField(max_length=30)
    class Meta:
        verbose_name = "armário"

    def __str__(self):
        return str(self.nome)

class Sensor(models.Model):
    nome = models.CharField(max_length=30)
    codigoAPI = models.PositiveIntegerField("Código do sensor na API", help_text="Código do sensor na API que recebe as leituras do sistema embarcado de monitoramento.")
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
class RegistroSaida(models.Model):
    data = models.DateTimeField('Data da saída', default=timezone.now)
    descricao = models.CharField('Justificativa da saída', max_length=300)
    destino = models.CharField('Destino', max_length=50)
    class Meta:
        verbose_name = "registro de saída"

class Recipiente(models.Model):
    quantidade = models.DecimalField(max_digits=7, decimal_places=2)
    qrCode = models.ImageField(upload_to='qrcodes', null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    posicao = models.ForeignKey(Posicao, on_delete=models.CASCADE)
    registroEntrada = models.ForeignKey(RegistroEntrada, on_delete=models.CASCADE)
    registroSaida = models.ForeignKey(RegistroSaida, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.pk)
    
    def gerarQrCode(self, url):
        name = f"{self.id}_qrCode.png"
        qr = qrcode.QRCode(version = 1, box_size = 10, border = 0)
        qr.add_data(url)
        qr.make(fit = True)
        qr_image = qr.make_image(fill_color = 'black', back_color = 'white')
        stream = BytesIO()
        qr_image.save(stream, 'PNG')
        self.qrCode.save(name, File(stream), save=False)
        self.save()           
class Teste(models.Model):
    data = models.DateTimeField('Data de realização do teste', default=timezone.now)
    observacoes = models.CharField('Observações gerais sobre o teste', max_length=300, blank=True)
    local = models.CharField('Local de realização do teste', max_length=50)
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="responsável")
class TesteTransgenia(Teste):
    resultado = models.BooleanField("Transgênico?", default=False)

    def __str__(self):
        return str(f"Teste de transgenia - {self.pk}")
    class Meta:
        verbose_name = "teste de transgenia"
        verbose_name_plural = "testes de transgenia"
class TesteUmidade(Teste):
    resultado = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(f"Teste de umidade - {self.pk}")
    class Meta:
        verbose_name = "teste de umidade"
        verbose_name_plural = "testes de umidade"
class TesteGerminacao(Teste):
    resultado = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(f"Teste de germinação - {self.pk}")
    class Meta:
        verbose_name = "teste de germinação"
        verbose_name_plural = "testes de germinação"
