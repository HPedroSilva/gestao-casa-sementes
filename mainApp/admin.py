from django.contrib import admin
from mainApp.models import *
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from django.shortcuts import redirect
from django.urls import reverse
from django import forms
class EnderecoInline(admin.StackedInline):
    model = Endereco
    max_num = 3
@admin.register(Guardiao)
class GuardiaoAdmin(admin.ModelAdmin):
    inlines = [EnderecoInline,]

class RecipienteInline(admin.StackedInline):
    model = Recipiente
    exclude = ["registroSaida", "qrCode"]
    extra = 1
@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = ("data", "safra", "descricao", "guardiao", "variedade", "enderecoGuardiao")
    inlines = [RecipienteInline,]
    dynamic_fields = ("enderecoGuardiao",)

    def get_dynamic_enderecoGuardiao_field(self, data):
        guardiao = data.get("guardiao")
        value = data.get("enderecoGuardiao")
        if not guardiao:
            queryset = Endereco.objects.none()
            value = None
        else:
            queryset = Endereco.objects.filter(guardiao=guardiao)
            if value == None:
                value = queryset.first()
        hidden = not queryset.exists()
        return queryset, value, hidden
        
    def response_add(self, request, obj, post_url_continue=None): # Redirecionar para página de impressão de etiquetas após adicionar um registro
        registroEntrada = obj
        recipientes = Recipiente.objects.filter(registroEntrada=obj)
        for recipiente in recipientes:
            recipiente.gerarQrCode(request.build_absolute_uri(reverse('mainApp:recipiente', args=[recipiente.id])))
        return redirect(reverse('mainApp:etiquetas_registro_entrada', args=[obj.id]))
    
    def response_change(self, request, obj):  # Redirecionar para página de impressão de etiquetas após editar um registro
        registroEntrada = obj
        recipientes = Recipiente.objects.filter(registroEntrada=obj)
        for recipiente in recipientes:
            recipiente.gerarQrCode(request.build_absolute_uri(reverse('mainApp:recipiente', args=[recipiente.id])))
        return redirect(reverse('mainApp:etiquetas_registro_entrada', args=[obj.id]))
class RegistroSaidaForm(forms.ModelForm):
    recipientes = forms.ModelMultipleChoiceField(Recipiente.objects.filter(registroSaida=None))
    class Meta:
        model = RegistroSaida
        fields = ["data", "descricao", "destino"]
@admin.register(RegistroSaida)
class RegistroSaidaAdmin(admin.ModelAdmin):
    form = RegistroSaidaForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            registroSaida = form.save()
            recipientes = form.cleaned_data['recipientes']
            for recipiente in recipientes:
                recipiente.registroSaida = registroSaida
                recipiente.save()
        super().save_model(request, obj, form, change)

admin.site.register(Especie)
admin.site.register(Variedade)
admin.site.register(Armario)
admin.site.register(Sensor)
admin.site.register(Posicao)
admin.site.register(Unidade)
admin.site.register(TesteGerminacao)
admin.site.register(TesteTransgenia)
admin.site.register(TesteUmidade)
admin.site.register(Recipiente)