from django.contrib import admin
from mainApp.models import *
class EnderecoInline(admin.StackedInline):
    model = Endereco
    max_num = 3
class GuardiaoAdmin(admin.ModelAdmin):
    inlines = [EnderecoInline,]

admin.site.register(Especie)
admin.site.register(Variedade)
admin.site.register(Guardiao, GuardiaoAdmin)
admin.site.register(RegistroEntrada)
admin.site.register(Armario)
admin.site.register(Sensor)
admin.site.register(Posicao)
admin.site.register(Unidade)
admin.site.register(RegistroSaida)
admin.site.register(TipoTeste)
admin.site.register(Teste)



