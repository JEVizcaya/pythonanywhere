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
    list_display = ('equipo_local', 'logo_local_preview', 'equipo_visitante', 'logo_rival_preview', 'fecha', 'estadio', 'jornada', 'goles_local', 'goles_visitante')
    list_filter = ('fecha', 'temporada', 'jornada', 'equipo_local', 'equipo_visitante')

    def logo_local_preview(self, obj):
        from django.utils.html import format_html
        if obj.logo_local:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo_local.url)
        return None
    logo_local_preview.short_description = 'Logo Local'

    def logo_rival_preview(self, obj):
        from django.utils.html import format_html
        if obj.logo_rival:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo_rival.url)
        return None
    logo_rival_preview.short_description = 'Logo Rival'
