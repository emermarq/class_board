from django.contrib import admin

from grade.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'turma', 'componente_curricular', 'professor', 'inicio', 'fim')
    list_filter = ('dia_semana', 'turma', 'componente_curricular', 'professor')

# Register your models here.
