from mainApp.models import Recipiente, Variedade, Unidade
from django.db.models import Sum

def getUnidades():
    '''
    Retorna todas as unidades cadastradas
    '''
    unidades = Unidade.objects.all()
    return unidades

def getSementes():
    '''
    Retorna quais as variedades estão presentes na casa de sementes e sua quantidade por cada unidade cadastrada no sistema.
    '''
    qtdSementes = {}
    variedades = Variedade.objects.all()
    unidades = getUnidades()
    for unidade in unidades:
        qtdVariedade = []
        for variedade in variedades:
            qtd = Recipiente.objects.filter(registroEntrada__variedade__nome = variedade.nome).filter(unidade=unidade).aggregate(Sum('quantidade'))['quantidade__sum']
            if qtd:
                qtdVariedade.append([variedade.nome, qtd])
        if qtdVariedade:
            qtdSementes[unidade] = qtdVariedade
    return(qtdSementes)

