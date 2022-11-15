from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "mainApp"
urlpatterns = [
    path('recipiente/<int:id_recipiente>/', login_required(views.RecipienteView.as_view()), name='recipiente'),
    path('etiqueta-recipiente/<int:id_recipiente>/', login_required(views.EtiquetaRecipienteView.as_view()), name='etiqueta_recipiente'),
    path('etiquetas-registro/<int:id_registro_entrada>/', login_required(views.EtiquetasRegistroView.as_view()), name='etiquetas_registro_entrada'),
    path('dashboard/', login_required(views.DashboardView.as_view()), name='dashboard'),
    path('registro-entrada/<int:id_registro>/', login_required(views.RegistroEntradaView.as_view()), name='registro_entrada'),
    path('registros-entrada/', login_required(views.RegistrosEntradaView.as_view()), name='registros_entrada'),
    path('recipientes/', login_required(views.RecipientesView.as_view()), name='recipientes'),
    path('testes/', login_required(views.TestesView.as_view()), name='testes'),
    path('testes-umidade/', login_required(views.TestesUmidadeView.as_view()), name='testes_umidade'),
    path('testes-germinacao/', login_required(views.TestesGerminacaoView.as_view()), name='testes_germinacao'),
    path('testes-transgenia/', login_required(views.TestesTransgeniaView.as_view()), name='testes_transgenia'),
    path('configuracoes/', login_required(views.ConfiguracoesView.as_view()), name='configuracoes'),
    
    path('atualizar-qrcode-recipientes/', login_required(views.AtualizarQrcodeRecipientesView), name='atualizar_qrcode_recipientes'),
]