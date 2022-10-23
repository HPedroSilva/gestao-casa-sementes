from django.urls import path
from . import views

app_name = "mainApp"
urlpatterns = [
    path('recipiente/<int:id_recipiente>/', views.RecipienteView.as_view(), name='recipiente'),
    path('etiqueta-recipiente/<int:id_recipiente>/', views.EtiquetaRecipienteView.as_view(), name='etiqueta_recipiente'),
    path('etiquetas-registro/<int:id_registro_entrada>/', views.EtiquetasRegistroView.as_view(), name='etiquetas_registro_entrada'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]