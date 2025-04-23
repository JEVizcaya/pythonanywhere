from django.contrib import admin
from .models import Noticia,Jugador
from django.contrib.auth.admin import UserAdmin

admin.site.register(Noticia)
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dorsal', 'posicion', 'nacionalidad', 'altura', 'pie_preferido')
    search_fields = ('nombre', 'posicion', 'nacionalidad')
    list_filter = ('posicion', 'nacionalidad')



