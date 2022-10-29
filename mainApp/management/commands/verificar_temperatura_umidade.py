import kronos
from django.core.management.base import BaseCommand
from datetime import datetime
from django.conf import settings
from mainApp.tools.leitura import jsonToLeituras
from mainApp.tools.notificacoes import alertaTemperaturaAlta, alertaTemperaturaBaixa, alertaUmidadeAlta, alertaUmidadeBaixa
import requests

@kronos.register("*/1 * * * *")
class Command(BaseCommand):
    help=""
    temp_max = 27.0 # Estabelecer esses valores como valores de configuração do sistema
    temp_min = 21.0
    umidade_max = 80.0
    umidade_min = 50.0
    def handle(self, *args, **options):
        """
        """
        print("Verificando temperatura e umidade")
        alertaTemperaturaAlta("leitura")

        try:
            res = requests.get(f"{settings.API_URL}last?sensores=1,2,3") # Mudar os ids dos sensores para uma consulta aos sensores cadastrados.
            leituras = jsonToLeituras(res.json())
            for leitura in leituras:
                print(leitura)
                print(leitura.temperatura)
                if(leitura.temperatura < self.temp_min):
                    alertaTemperaturaBaixa(leitura)
                elif(leitura.temperatura > self.temp_max):
                    alertaTemperaturaAlta(leitura)
                    print("Alerta alta")

                if(leitura.umidade < self.umidade_min):
                    alertaUmidadeBaixa(leitura)
                elif(leitura.umidade > self.umidade_max):
                    alertaUmidadeAlta(leitura)
        except:
            pass # Fazer alguma lógica de notificação de erro com maior prazo (contar quantos erros aconteceram, se passar de um valor determinado manda uma notificação)