from django.shortcuts import render
from django.views.generic.base import TemplateView
from mainApp.models import Recipiente
from django.shortcuts import get_object_or_404

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