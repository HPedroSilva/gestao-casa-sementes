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
    path('configuracoes/', login_required(views.ConfiguracoesView.as_view()), name='configuracoes'),
    
    path('atualizar-qrcode-recipientes/', login_required(views.AtualizarQrcodeRecipientesView), name='atualizar_qrcode_recipientes'),
]