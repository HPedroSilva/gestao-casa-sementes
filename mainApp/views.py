from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib import messages
from mainApp.models import Recipiente, RegistroEntrada
from mainApp.forms import ConfiguracoesForm
from django.shortcuts import get_object_or_404
from mainApp.tools.leitura import jsonToLeituras, calcMedia
from datetime import datetime, timedelta
from mainApp.functions import getSementes, getUnidades
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
import requests
import json
import os.path
class RecipienteView(TemplateView):
    template_name = "recipiente.html"
    recipiente = None
    registroEntrada = None
    def get(self, request, *args, **kwargs):
        pk_recipiente = int(kwargs.get('id_recipiente', 0))
        self.recipiente = get_object_or_404(Recipiente, pk = pk_recipiente)
        return super(RecipienteView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipiente'] = self.recipiente
        return context
class EtiquetaRecipienteView(TemplateView):
    template_name = "etiquetaRecipiente.html"
    recipiente = None
    registroEntrada = None
    def get(self, request, *args, **kwargs):
        pk_recipiente = int(kwargs.get('id_recipiente', 0))
        self.recipiente = get_object_or_404(Recipiente, pk = pk_recipiente)
        return super(EtiquetaRecipienteView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipiente'] = self.recipiente
        return context

class EtiquetasRegistroView(TemplateView):
    template_name = "etiquetasRegistro.html"
    registroEntrada = None
    recipientes = None
    def get(self, request, *args, **kwargs):
        pkRegistroEntrada = int(kwargs.get('id_registro_entrada', 0))
        self.registroEntrada = get_object_or_404(RegistroEntrada, pk = pkRegistroEntrada)
        self.recipientes = self.registroEntrada.recipiente_set.all()
        return super(EtiquetasRegistroView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registroEntrada'] = self.registroEntrada
        context['recipientes'] = self.recipientes
        return context
class DashboardView(TemplateView):
    template_name = "dashboard.html"
    tempMedia = 0 
    umidadeMedia = 0
    erroLeituras = False
    erroUltLeituras = False
    leituras = []
    ultLeituras = []
    def get(self, request, *args, **kwargs):
        try:
            res = requests.get("http://localhost:3000/last?sensores=1,2,3&qtdLeituras=3")
            self.ultLeituras = jsonToLeituras(res.json())
            self.tempMedia, self.umidadeMedia = calcMedia(self.ultLeituras)
        except:
            self.erroUltLeituras = True
        try:
            now = datetime.utcnow().isoformat()
            yest = (datetime.utcnow() - timedelta(days=1)).isoformat()
            res = requests.get(f"http://localhost:3000/last-date?start={yest}&end={now}")
            self.leituras = jsonToLeituras(res.json())
        except:
            self.erroLeituras = True
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tempMedia'] = self.tempMedia
        context['umidadeMedia'] = self.umidadeMedia
        context['ultLeituras'] = self.ultLeituras
        context['leituras'] = self.leituras
        context['erroUltLeituras'] = self.erroUltLeituras
        context['erroLeituras'] = self.erroLeituras
        context['qtdSementes'] = getSementes()
        context['unidades'] = getUnidades()
        return context

class RegistroEntradaView(TemplateView):
    template_name = "registroEntrada.html"
    recipientes = []
    registroEntrada = RegistroEntrada.objects.none
    def get(self, request, *args, **kwargs):
        pkRegistroEntrada = int(kwargs.get('id_registro', 0))
        if(pkRegistroEntrada):
            self.registroEntrada = get_object_or_404(RegistroEntrada, pk = pkRegistroEntrada)
            self.recipientes = self.registroEntrada.recipiente_set.all()
        return super(RegistroEntradaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(self.recipientes):
            context['object_list'] = self.recipientes
        context['registroEntrada'] = self.registroEntrada
        return context
class RegistrosEntradaView(ListView):
    template_name = "listRegistrosEntrada.html"
    model = RegistroEntrada
class RecipientesView(ListView):
    template_name = "listRecipientes.html"
    model = Recipiente
    recipientes = []
    registroEntrada = RegistroEntrada.objects.none
    def get(self, request, *args, **kwargs):
        pkRegistroEntrada = int(request.GET.get('registro', 0))
        if(pkRegistroEntrada):
            self.registroEntrada = get_object_or_404(RegistroEntrada, pk = pkRegistroEntrada)
            self.recipientes = self.registroEntrada.recipiente_set.all()
        return super(RecipientesView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(self.recipientes):
            context['object_list'] = self.recipientes
        context['registroEntrada'] = self.registroEntrada
        return context
class ConfiguracoesView(FormView):
    template_name = 'configuracoes.html'
    form_class = ConfiguracoesForm 
    success_url = '/mainapp/configuracoes'

    configuracoesFileEscrita = settings.CONFIGURACOES_FILE    
    if os.path.isfile(settings.CONFIGURACOES_FILE):
        configuracoesFileLeitura = settings.CONFIGURACOES_FILE
    else:
        configuracoesFileLeitura = settings.CONFIGURACOES_DEFAULT_FILE

    def get_initial(self):
        initial = super().get_initial()

        with open(self.configuracoesFileLeitura) as jsonConfiguracoes:
            configuracoes = json.load(jsonConfiguracoes)

        initial["temperaturaMin"] =  configuracoes["temperaturaMin"]
        initial["temperaturaMax"] = configuracoes["temperaturaMax"]
        initial["umidadeMax"] = configuracoes["umidadeMax"]
        initial["umidadeMin"] = configuracoes["umidadeMin"]
        initial["freqTesteUmidade"] = configuracoes["freqTesteUmidade"]
        initial["freqTesteGerminacao"] = configuracoes["freqTesteGerminacao"]
        initial["freqTesteTransgenia"] = configuracoes["freqTesteTransgenia"]
        initial["urlAPI"] = configuracoes["urlAPI"]

        return initial
    
    def form_valid(self, form):
        data = form.cleaned_data

        configuracoes = {}
        configuracoes["temperaturaMin"] =  float(data["temperaturaMin"])
        configuracoes["temperaturaMax"] = float(data["temperaturaMax"])
        configuracoes["umidadeMax"] = float(data["umidadeMax"])
        configuracoes["umidadeMin"] = float(data["umidadeMin"])
        configuracoes["freqTesteUmidade"] = data["freqTesteUmidade"]
        configuracoes["freqTesteGerminacao"] = data["freqTesteGerminacao"]
        configuracoes["freqTesteTransgenia"] = data["freqTesteTransgenia"]
        configuracoes["urlAPI"] = data["urlAPI"]

        with open(self.configuracoesFileEscrita, "w") as jsonConfiguracoes:
            json.dump(configuracoes, jsonConfiguracoes)

        messages.success(self.request, 'Configurações atualizadas com sucesso!')

        return super().form_valid(form)
        
def AtualizarQrcodeRecipientesView(request):
    if request.GET['recipientes']:
        stringRecipientes = request.GET['recipientes']
        recipientesList = list(map(int, stringRecipientes.split(',')))
        recipientes = Recipiente.objects.filter(pk__in = recipientesList)
        for recipiente in recipientes:
            recipiente.gerarQrCode(request.build_absolute_uri(reverse('mainApp:recipiente', args=[recipiente.id])))
    return HttpResponse(status=200)
