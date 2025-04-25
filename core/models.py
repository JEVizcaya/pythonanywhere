from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# Create your models here.
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios_generales')  # Cambié 'comentarios' por 'comentarios_generales'
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.noticia.titulo}'
    
class Jugador(models.Model):
    POSICIONES = [
        ('POR', 'Portero'),
        ('DEF', 'Defensa'),
        ('MED', 'Centrocampista'),
        ('DEL', 'Delantero'),
    ]

    nombre_completo = models.CharField(max_length=100)
    dorsal = models.PositiveIntegerField()
    posicion = models.CharField(max_length=3, choices=POSICIONES)
    foto = models.ImageField(upload_to='jugadores/')
    fecha_nacimiento = models.DateField(null=True)
    lugar_nacimiento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    bandera = models.ImageField(upload_to='banderas/')
    altura = models.DecimalField(max_digits=4, decimal_places=2)  # Ej: 1.83
    pie_preferido = models.CharField(max_length=10)
    fin_contrato = models.DateField()

    def __str__(self):
        return f"{self.nombre_completo} ({self.get_posicion_display()})"

    def lugar_completo(self):
        return f"{self.lugar_nacimiento} ({self.provincia})"
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return (
                today.year
                - self.fecha_nacimiento.year
                - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            )
        return "Desconocida"
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nombre   
class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)
    fecha = models.DateTimeField()
    jornada = models.IntegerField(null=True, blank=True)
    estadio = models.CharField(max_length=200, null=True, blank=True)
    temporada = models.CharField(max_length=9, default="2024-2025") # Añade un campo para la temporada
    # ... otros campos que puedas tener ...

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} ({self.fecha})"
    
class ComentarioNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios_especiales')  # Cambié 'comentarios' por 'comentarios_especiales'
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.noticia.titulo}'
    
