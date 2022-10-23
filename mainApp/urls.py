from django.urls import path
from . import views

app_name = "mainApp"
urlpatterns = [
    path('recipiente/<int:id_recipiente>/', views.RecipienteView.as_view(), name='recipiente'),
]