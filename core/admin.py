from django.contrib import admin
from .models import Noticia, Jugador, Partido, ComentarioNoticia, Comentario,Equipo
from django.utils.safestring import mark_safe

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

class PartidoAdmin(admin.ModelAdmin):
    list_display = ('logo_local_preview', 'equipo_local', 'goles_local', 'goles_visitante', 'equipo_visitante', 'logo_visitante_preview', 'fecha', 'jornada', 'estadio')

    def logo_local_preview(self, obj):
        if obj.equipo_local and obj.equipo_local.logo:
            return mark_safe(f'<img src="{obj.equipo_local.logo.url}" width="50" height="50" />')
        return '-'
    logo_local_preview.short_description = 'Logo Local'

    def logo_visitante_preview(self, obj):
        if obj.equipo_visitante and obj.equipo_visitante.logo:
            return mark_safe(f'<img src="{obj.equipo_visitante.logo.url}" width="50" height="50" />')
        return '-'
    logo_visitante_preview.short_description = 'Logo Visitante'

admin.site.register(Equipo)
admin.site.register(Partido, PartidoAdmin)