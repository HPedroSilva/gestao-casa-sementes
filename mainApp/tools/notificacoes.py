from notifications.signals import notify
from django.contrib.auth.models import Group
from mainApp.models import Sensor
import json

def notificar(msg, valor, valorMax):
    grupo = Group.objects.get(pk=1) # Mudar para um campo do arquivo de configurações do sistema
    usuarios = grupo.user_set.all()
    sensor = Sensor.objects.get(pk=1)
    verb = {
        "msg": msg,
        "valor": valor,
        "valorMax": valorMax
    }
    
    for usuario in usuarios:
        notify.send(usuario, recipient=grupo, verb=json.dumps(verb), target=sensor, level='warning') # Mudar recipient para um grupo de usuários específico

def notificarTemperaturaAlta(temp, tempMax):
    notificar("Temperatura acima da temperatura ideal.", temp, tempMax)

def notificarTemperaturaBaixa(temp, tempMin):
    notificar("Temperatura abixo da temperatura ideal.", temp, tempMin)

def notificarUmidadeAlta(umidade, umidadeMax):
    notificar("Umidade acima da umidade ideal.", umidade, umidadeMax)

def notificarUmidadeBaixa(umidade, umidadeMin):
    notificar("Umidade abaixo da umidade ideal.", umidade, umidadeMin)
