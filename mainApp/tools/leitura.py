from datetime import datetime

class Leitura():
    def __init__(self, id, erro, sensorId, temperatura, umidade, data, cloudSaved) -> None:
        self.id = id
        self.erro = erro
        self.sensorId = sensorId
        self.temperatura = temperatura
        self.umidade = umidade
        self.data = datetime.strptime(data,"%Y-%m-%dT%H:%M:%S.%fZ")
        self.cloudSaved = cloudSaved
    
    def __str__(self) -> str:
        return str(self.id)

def jsonToLeituras(json):
    '''
    Converte os dados de leituras recebidas em json para uma lista de objetos do tipo Leitura
    '''
    leituras = []
    if json:
        for i in json:
            if i['erro'] and i['erro'] != "Not found":
                leitura = Leitura(i['_id'], i['erro'], i['sensorId'], i['temperatura'], i['umidade'], i['data'], i['cloudSaved'])
                leituras.append(leitura)
    return leituras

def calcMedia(leituras):
    '''
    Calcula a temperatura e umidade média das leituras recebidas
    '''
    tempMedia = 0 
    umidadeMedia = 0
    listTemp = []
    listUmidade = []
    for i in leituras:
        if i.erro and i.erro == "OK":
            listTemp.append(float(i.temperatura))
            listUmidade.append(float(i.umidade))
    tempMedia = sum(listTemp) / len(listTemp)
    umidadeMedia = sum(listUmidade) / len(listUmidade)
    return tempMedia, umidadeMedia