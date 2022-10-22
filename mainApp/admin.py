from django.contrib import admin
from mainApp.models import *
from dynamic_admin_forms.admin import DynamicModelAdminMixin
class EnderecoInline(admin.StackedInline):
    model = Endereco
    max_num = 3
class GuardiaoAdmin(admin.ModelAdmin):
    inlines = [EnderecoInline,]

@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = ("data", "safra", "descricao", "guardiao", "variedade", "enderecoGuardiao")
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

admin.site.register(Especie)
admin.site.register(Variedade)
admin.site.register(Guardiao, GuardiaoAdmin)
admin.site.register(Armario)
admin.site.register(Sensor)
admin.site.register(Posicao)
admin.site.register(Unidade)
admin.site.register(RegistroSaida)
admin.site.register(TipoTeste)
admin.site.register(Teste)



