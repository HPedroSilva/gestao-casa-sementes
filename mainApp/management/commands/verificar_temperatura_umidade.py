import kronos
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.conf import settings
from mainApp.tools.leitura import jsonToLeituras
from mainApp.tools.notificacoes import alertaTemperaturaAlta, alertaTemperaturaBaixa, alertaUmidadeAlta, alertaUmidadeBaixa
import requests

@kronos.register("*/5 * * * *")
class Command(BaseCommand):
    help=""
    def handle(self, *args, **options):
        """
        """
        # Estabelecer esses valores abaixo como valores de configuração do sistema
        temp_max = 27.0 
        temp_min = 21.0
        umidade_max = 80.0
        umidade_min = 50.0
        intervalo_max = timedelta(minutes=5)
        
        agora = datetime.now()
        listTemp = []
        listUmidade = []
        
        try:
            res = requests.get(f"{settings.API_URL}last?sensores=1,2&qtdLeituras=5") # Mudar os ids dos sensores para uma consulta aos sensores cadastrados.
            leituras = jsonToLeituras(res.json())
            for leitura in leituras:
                if(leitura.data > agora - intervalo_max):
                    print(leitura.data)
                    listTemp.append(leitura.temperatura)
                    listUmidade.append(leitura.umidade)
            
            if listTemp: # Verificar também porque a lista está vazia e mandar um outro tipo de notificação (não está conseguindo comunicar com a API, por exemplo)
                tempMedia = sum(listTemp) / len(listTemp)
            if listUmidade: # Verificar também porque a lista está vazia e mandar um outro tipo de notificação (não está conseguindo comunicar com a API, por exemplo)
                umidadeMedia = sum(listUmidade) / len(listUmidade)

            if(tempMedia < temp_min):
                alertaTemperaturaBaixa(tempMedia)
            elif(tempMedia > temp_max):
                alertaTemperaturaAlta(tempMedia)

            if(umidadeMedia < umidade_min):
                alertaUmidadeBaixa(umidadeMedia)
            elif(umidadeMedia > umidade_max):
                alertaUmidadeAlta(umidadeMedia)
        
        except:
            pass # Fazer alguma lógica de notificação de erro com maior prazo (contar quantos erros aconteceram, se passar de um valor determinado manda uma notificação)