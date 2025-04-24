
from django.utils import timezone
from .models import Noticia,Comentario,Jugador,Partido
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
    proximos_partidos = Partido.objects.filter(fecha__gte=datetime.now())
    return render(request, 'encuentros/partidos.html', {'partidos': proximos_partidos})
def clasificacion(request):
    return render(request, 'encuentros/clasificacion.html')  # Asegúrate de tener un archivo clasificacion.html