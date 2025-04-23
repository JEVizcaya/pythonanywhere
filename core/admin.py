from django.contrib import admin
from .models import Noticia, Jugador, Partido, ComentarioNoticia, Comentario

admin.site.register(Noticia)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'autor', 'noticia', 'fecha_comentario')
    list_filter = ('fecha_comentario', 'noticia')
    search_fields = ('contenido', 'autor__username')

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dorsal', 'posicion', 'nacionalidad', 'altura', 'pie_preferido')
    search_fields = ('nombre', 'posicion', 'nacionalidad')
    list_filter = ('posicion', 'nacionalidad')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('rival', 'fecha', 'estadio')
    list_filter = ('fecha',)
