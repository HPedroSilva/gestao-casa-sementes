from notifications.signals import notify
from django.contrib.auth.models import User

def alertaTemperaturaAlta(leitura):
    user = User.objects.get(pk=1)
    notify.send(user, recipient=user, verb='Temperatura acima da temperatura ideal.') # Mudar recipient para um grupo de usuários específico

def alertaTemperaturaBaixa(leitura):
    pass

def alertaUmidadeBaixa(leitura):
    pass

def alertaUmidadeAlta(leitura):
    pass
