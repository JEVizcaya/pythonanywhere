
from django.utils import timezone
from .models import Noticia,Comentario,Jugador,Partido, Equipo
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import ComentarioForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistroForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from core.models import Partido, Equipo
from django.db.models import Q, F
from django.db import models




# Create your views here.

def home(request):
    return render(request, 'home.html', {'now': timezone.now()})

def lista_noticias(request):
    
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')  # Ordenar por fecha descendente
    return render(request, 'noticias/lista_noticias.html', {'noticias': noticias})



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige a la página de login después del registro
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')  # por si alguien accede por GET
    
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

@login_required
def editar_perfil_view(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = noticia
            comentario.autor = request.user  # Cambié 'usuario' por 'autor'
            comentario.save()
            return redirect('detalle_noticia', noticia_id=noticia.id)
    else:
        form = ComentarioForm()

    comentarios = noticia.comentarios_generales.all().order_by('-fecha_comentario')

    return render(request, 'noticias/detalle_noticia.html', {
        'noticia': noticia,
        'form': form,
        'comentarios': comentarios
    })
def historia_view(request):
    return render(request, 'historia.html')

def plantilla(request):
    jugadores = Jugador.objects.all()
    context = {
        'porteros': jugadores.filter(posicion='POR'),
        'defensas': jugadores.filter(posicion='DEF'),
        'medios': jugadores.filter(posicion='MED'),
        'delanteros': jugadores.filter(posicion='DEL'),
    }
    return render(request, 'jugadores/plantilla.html', context)

def detalle_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    return render(request, 'jugadores/detalle_jugador.html', {'jugador': jugador})

def partidos(request):
    try:
        celta = Equipo.objects.get(nombre__icontains='celta') # Busca un equipo que contenga 'celta' en su nombre
    except Equipo.DoesNotExist:
        # Manejar el caso en que no se encuentra el Celta
        partidos_celta_finalizados = Partido.objects.none()
        proximos_partidos_celta = Partido.objects.none()
    else:
        partidos_celta_finalizados = Partido.objects.filter(
            (models.Q(equipo_local=celta) | models.Q(equipo_visitante=celta)),
            fecha__lt=timezone.now()
        ).order_by('jornada') # Ordenamos los partidos finalizados por jornada

        proximos_partidos_celta = Partido.objects.filter(
            (models.Q(equipo_local=celta) | models.Q(equipo_visitante=celta)),
            fecha__gte=timezone.now()
        ).order_by('fecha') # Los próximos partidos los mantenemos ordenados por fecha

    context = {
        'partidos_finalizados': partidos_celta_finalizados,
        'proximos_partidos': proximos_partidos_celta,
    }
    return render(request, 'encuentros/partidos.html', context)
def clasificacion(request):
    temporada_seleccionada = request.GET.get('temporada', '2024-2025')
    equipos = Equipo.objects.all()
    clasificacion_data = []

    for equipo in equipos:
        # Filtramos solo los partidos con goles registrados (ya jugados)
        partidos_jugados = Partido.objects.filter(
            (Q(equipo_local=equipo) | Q(equipo_visitante=equipo)),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,  # Aseguramos que el partido tenga goles
            goles_visitante__isnull=False  # Aseguramos que el partido tenga goles
        ).count()

        partidos_ganados = Partido.objects.filter(
            (Q(equipo_local=equipo, goles_local__gt=F('goles_visitante')) | 
            Q(equipo_visitante=equipo, goles_visitante__gt=F('goles_local'))),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,
            goles_visitante__isnull=False
        ).count()

        partidos_empatados = Partido.objects.filter(
            (Q(equipo_local=equipo, goles_local=F('goles_visitante')) | 
            Q(equipo_visitante=equipo, goles_visitante=F('goles_local'))),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,
            goles_visitante__isnull=False
        ).count()

        partidos_perdidos = partidos_jugados - partidos_ganados - partidos_empatados
        
        goles_favor = Partido.objects.filter(
            equipo_local=equipo, 
            temporada=temporada_seleccionada,
            goles_local__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_local'))['sum_goles'] or 0
        
        goles_favor += Partido.objects.filter(
            equipo_visitante=equipo, 
            temporada=temporada_seleccionada,
            goles_visitante__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_visitante'))['sum_goles'] or 0

        goles_contra = Partido.objects.filter(
            equipo_local=equipo, 
            temporada=temporada_seleccionada,
            goles_visitante__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_visitante'))['sum_goles'] or 0
        
        goles_contra += Partido.objects.filter(
            equipo_visitante=equipo, 
            temporada=temporada_seleccionada,
            goles_local__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_local'))['sum_goles'] or 0

        diferencia_goles = goles_favor - goles_contra
        puntos = partidos_ganados * 3 + partidos_empatados

        clasificacion_data.append({
            'equipo': equipo,
            'pj': partidos_jugados,
            'pg': partidos_ganados,
            'pe': partidos_empatados,
            'pp': partidos_perdidos,
            'gf': goles_favor,
            'gc': goles_contra,
            'dg': diferencia_goles,
            'pts': puntos,
        })

    # Ordenamos la clasificación
    clasificacion_ordenada = sorted(clasificacion_data, key=lambda x: (-x['pts'], -x['dg'], -x['gf']))

    context = {
        'clasificacion': clasificacion_ordenada,
        'temporada_seleccionada': temporada_seleccionada,
    }
    return render(request, 'encuentros/clasificacion.html', context)
def clasificacion(request):
    temporada_seleccionada = request.GET.get('temporada', '2024-2025')
    equipos = Equipo.objects.all()
    clasificacion_data = []

    for equipo in equipos:
        # Filtramos solo los partidos con goles registrados (ya jugados)
        partidos_jugados = Partido.objects.filter(
            (Q(equipo_local=equipo) | Q(equipo_visitante=equipo)),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,  # Aseguramos que el partido tenga goles
            goles_visitante__isnull=False  # Aseguramos que el partido tenga goles
        ).count()

        partidos_ganados = Partido.objects.filter(
            (Q(equipo_local=equipo, goles_local__gt=F('goles_visitante')) | 
            Q(equipo_visitante=equipo, goles_visitante__gt=F('goles_local'))),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,
            goles_visitante__isnull=False
        ).count()

        partidos_empatados = Partido.objects.filter(
            (Q(equipo_local=equipo, goles_local=F('goles_visitante')) | 
            Q(equipo_visitante=equipo, goles_visitante=F('goles_local'))),
            temporada=temporada_seleccionada,
            goles_local__isnull=False,
            goles_visitante__isnull=False
        ).count()

        partidos_perdidos = partidos_jugados - partidos_ganados - partidos_empatados
        
        goles_favor = Partido.objects.filter(
            equipo_local=equipo, 
            temporada=temporada_seleccionada,
            goles_local__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_local'))['sum_goles'] or 0
        
        goles_favor += Partido.objects.filter(
            equipo_visitante=equipo, 
            temporada=temporada_seleccionada,
            goles_visitante__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_visitante'))['sum_goles'] or 0

        goles_contra = Partido.objects.filter(
            equipo_local=equipo, 
            temporada=temporada_seleccionada,
            goles_visitante__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_visitante'))['sum_goles'] or 0
        
        goles_contra += Partido.objects.filter(
            equipo_visitante=equipo, 
            temporada=temporada_seleccionada,
            goles_local__isnull=False
        ).aggregate(sum_goles=models.Sum('goles_local'))['sum_goles'] or 0

        diferencia_goles = goles_favor - goles_contra
        puntos = partidos_ganados * 3 + partidos_empatados

        clasificacion_data.append({
            'equipo': equipo,
            'pj': partidos_jugados,
            'pg': partidos_ganados,
            'pe': partidos_empatados,
            'pp': partidos_perdidos,
            'gf': goles_favor,
            'gc': goles_contra,
            'dg': diferencia_goles,
            'pts': puntos,
        })

    # Ordenamos la clasificación
    clasificacion_ordenada = sorted(clasificacion_data, key=lambda x: (-x['pts'], -x['dg'], -x['gf']))

    context = {
        'clasificacion': clasificacion_ordenada,
        'temporada_seleccionada': temporada_seleccionada,
    }
    return render(request, 'encuentros/clasificacion.html', context)


def resultados_por_jornada(request):
    jornada_seleccionada = request.GET.get('jornada', None)
    
    # Si no se ha seleccionado ninguna jornada, no mostrar partidos
    if jornada_seleccionada:
        # Filtrar partidos, excluyendo los del Celta (suponiendo que el nombre del equipo es "Celta")
        partidos = Partido.objects.exclude(equipo_local__nombre="Celta").exclude(equipo_visitante__nombre="Celta")
        partidos = partidos.filter(jornada=jornada_seleccionada)
    else:
        partidos = None  # No hay partidos si no se selecciona jornada

    # Obtenemos las jornadas disponibles para el select
    jornadas_disponibles = Partido.objects.values_list('jornada', flat=True).distinct()

    return render(request, 'encuentros/resultados.html', {
        'partidos': partidos,
        'jornadas_disponibles': jornadas_disponibles,
        'jornada_seleccionada': jornada_seleccionada,
    })