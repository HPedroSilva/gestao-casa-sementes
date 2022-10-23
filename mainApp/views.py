from dataclasses import dataclass
from django.shortcuts import render
from django.views.generic.base import TemplateView
from mainApp.models import Recipiente, RegistroEntrada
from django.shortcuts import get_object_or_404
from mainApp.tools.leitura import jsonToLeituras, calcMedia
import requests

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
    erroLeitura = False
    leituras = []
    def get(self, request, *args, **kwargs):
        try:
            res = requests.get("http://localhost:3000/last?sensores=1,2,3")
            self.leituras = jsonToLeituras(res.json())
            self.tempMedia, self.umidadeMedia = calcMedia(self.leituras)
        except:
            self.erroLeitura = True
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tempMedia'] = self.tempMedia
        context['umidadeMedia'] = self.umidadeMedia
        context['leituras'] = self.leituras
        context['erroLeitura'] = self.erroLeitura
        return context