from django.contrib import admin
from .models import Noticia,Jugador,Partido,ComentarioNoticia
from django.contrib.auth.admin import UserAdmin

admin.site.register(Noticia)

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dorsal', 'posicion', 'nacionalidad', 'altura', 'pie_preferido')
    search_fields = ('nombre', 'posicion', 'nacionalidad')
    list_filter = ('posicion', 'nacionalidad')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('rival', 'fecha', 'estadio')
    list_filter = ('fecha',)

@admin.register(ComentarioNoticia)
class ComentarioNoticiaAdmin(admin.ModelAdmin):
    list_display = ('autor', 'noticia', 'contenido', 'fecha_creacion')  # Agrega los campos que deseas ver en la tabla
    search_fields = ('autor__username', 'contenido')  # Permite buscar por autor o contenido
    list_filter = ('noticia', 'fecha_creacion')  # Filtros para la tabla en admin