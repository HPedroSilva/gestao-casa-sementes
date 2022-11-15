from django import forms

class ConfiguracoesForm(forms.Form):

    temperaturaMax = forms.DecimalField(label="Temperatura Máxima: ")
    temperaturaMin = forms.DecimalField(label="Temperatura Mínima: ")
    umidadeMax = forms.DecimalField(label="Umidade Máxima: ")
    umidadeMin = forms.DecimalField(label="Umidade Mínima: ")
    freqTesteUmidade = forms.IntegerField(label="Frequência do teste de umidade: ", max_value=10)
    freqTesteGerminacao = forms.IntegerField(label="Frequência do teste de germinação: ")
    freqTesteTransgenia = forms.IntegerField(label="Frequência do teste de trangenia: ")
    urlAPI = forms.URLField(label="URL para a API do sistema de monitoramento: ")

    def __init__(self, *args, **kwargs):
        super(ConfiguracoesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in self.errors:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'})