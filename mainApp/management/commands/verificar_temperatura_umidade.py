import kronos
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.conf import settings
from mainApp.tools.leitura import jsonToLeituras
from mainApp.tools.notificacoes import notificarTemperaturaAlta, notificarTemperaturaBaixa, notificarUmidadeAlta, notificarUmidadeBaixa
import requests

@kronos.register("*/5 * * * *")
class Command(BaseCommand):
    help=""
    def handle(self, *args, **options):
        """
        """
        # Estabelecer esses valores abaixo como valores de configuração do sistema
        tempMax = 35.0
        tempMin = 32.0
        umidadeMax = 30.0
        umidadeMin = 20.0
        intervaloMax = timedelta(minutes=5)
        
        agora = datetime.now()
        listTemp = []
        listUmidade = []
        
        try:
            res = requests.get(f"{settings.API_URL}last?sensores=1,2&qtdLeituras=5") # Mudar os ids dos sensores para uma consulta aos sensores cadastrados. De forma que a análise de temperatura seja feita de forma isolada para cada sensor.
            leituras = jsonToLeituras(res.json())
            for leitura in leituras:
                if(leitura.data > agora - intervaloMax):
                    listTemp.append(leitura.temperatura)
                    listUmidade.append(leitura.umidade)
            
            if listTemp: # Verificar também porque a lista está vazia e mandar um outro tipo de notificação (não está conseguindo comunicar com a API, por exemplo)
                tempMedia = sum(listTemp) / len(listTemp)
            if listUmidade: # Verificar também porque a lista está vazia e mandar um outro tipo de notificação (não está conseguindo comunicar com a API, por exemplo)
                umidadeMedia = sum(listUmidade) / len(listUmidade)

            if(tempMedia < tempMin):
                notificarTemperaturaBaixa(tempMedia, tempMin)
            elif(tempMedia > tempMax):
                notificarTemperaturaAlta(tempMedia, tempMax)

            if(umidadeMedia < umidadeMin):
                notificarUmidadeBaixa(umidadeMedia, umidadeMin)
            elif(umidadeMedia > umidadeMax):
                notificarUmidadeAlta(umidadeMedia, umidadeMax)
        
        except:
            pass # Fazer alguma lógica de notificação de erro com maior prazo (contar quantos erros aconteceram, se passar de um valor determinado manda uma notificação)