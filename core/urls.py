from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
]