from django.shortcuts import render
from django.utils import timezone
from .models import Noticia


# Create your views here.

def home(request):
    return render(request, 'home.html', {'now': timezone.now()})

def lista_noticias(request):
    
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')  # Ordenar por fecha descendente
    return render(request, 'noticias/lista_noticias.html', {'noticias': noticias})