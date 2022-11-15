from django import forms

class ConfiguracoesForm(forms.Form):

    # temperatura máx e min
    # umidade máx e min
    # frequencia de teste de umidade, germinacao e trangenia
    # endereço da API
    temperaturaMax = forms.DecimalField(label="Temperatura Máxima")
    temperaturaMin = forms.DecimalField()
    umidadeMax = forms.DecimalField()
    umidadeMin = forms.DecimalField()
    freqTesteUmidade = forms.IntegerField(max_value=10)
    freqTesteGerminacao = forms.IntegerField()
    freqTesteTransgenia = forms.IntegerField()
    urlAPI = forms.URLField()