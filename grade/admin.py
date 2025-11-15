from django.contrib import admin

from grade.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'turma', 'componente_curricular', 'professor', 'inicio', 'fim')
    list_filter = ('dia_semana', 'turma', 'componente_curricular', 'professor')

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grade"

    def __str__(self):
            return self.turma

# Register your models here.
