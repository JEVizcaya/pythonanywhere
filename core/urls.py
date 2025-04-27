from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import logout_view
from .views import editar_perfil_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.home, name='home'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticia/<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
    path('clasificacion/', views.clasificacion, name='clasificacion'),
    path('historia/', views.historia_view, name='historia'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('plantilla/', views.plantilla, name='plantilla'),
    path('jugador/<int:jugador_id>/', views.detalle_jugador, name='detalle_jugador'),
    path('partidos/', views.partidos, name='partidos'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='usuarios/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='usuarios/password_change_done.html'), name='password_change_done'),
    path('resultados/', views.resultados_por_jornada, name='resultados'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)