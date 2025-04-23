from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import logout_view
from .views import editar_perfil_view

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.home, name='home'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticia/<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
    path('historia/', views.historia_view, name='historia'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
]