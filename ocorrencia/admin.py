from django.contrib import admin
from .models import Professor_Ausente, Professor_Substituto


@admin.register(Professor_Ausente)
class Professor_AusenteAdmin(admin.ModelAdmin):
    list_display = ('inicio_formatada', 'professor','justificativa')
    list_filter = ('inicio',)

    def inicio_formatada(self, obj):
        return obj.inicio.strftime('%d/%m/%Y')

    inicio_formatada.short_description = 'Inicio'

    def fim_formatada(self, obj):
        return obj.fim.strftime('%d/%m/%Y')

    inicio_formatada.short_description = 'Fim'

@admin.register(Professor_Substituto)
class Professor_SubstitutoAdmin(admin.ModelAdmin):
    list_display = ('inicio_formatada', 'fim_formatada', 'ausente','substituto')
    list_filter = ('inicio',)

    def inicio_formatada(self, obj):
        return obj.inicio.strftime('%d/%m/%Y')

    inicio_formatada.short_description = 'Inicio'

    def fim_formatada(self, obj):
        return obj.fim.strftime('%d/%m/%Y')

    fim_formatada.short_description = 'Fim'
