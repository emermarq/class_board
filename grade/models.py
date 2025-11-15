from django.db import models
from home.models import Componente_Curricular, Professor, Turma


class Grade(models.Model):
    DIA_SEMANA = [
        ("Segunda-feira", "Segunda-feira"),
        ("Terça-feira", "Terça-feira"),
        ("Quarta-feira", "Quarta-feira"),
        ("Quinta-feira", "Quinta-feira"),
        ("Sexta-feira", "Sexta-feira"),
    ]
    dia_semana = models.CharField(max_length=20, choices=DIA_SEMANA, verbose_name="Dia Semana")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    componente_curricular = models.ForeignKey(Componente_Curricular, on_delete=models.CASCADE)
    inicio = models.TimeField()
    fim = models.TimeField()

    class Meta:
        db_table = 'grade'
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

# Create your models here.
