from django.db import models

from home.models import Professor, Justificativa


class Professor_Ausente(models.Model):
    inicio = models.DateField()
    fim = models.DateField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    justificativa = models.ForeignKey(Justificativa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Professor Ausente"
        verbose_name_plural = "Professor Ausente"

    def __str__(self):
        return self.inicio.strftime('%d/%m/%Y')


class Professor_Substituto(models.Model):
    inicio = models.DateField()
    fim = models.DateField()
    ausente = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="Professor_Ausente")
    substituto = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="Professor_Substituto")

    class Meta:
        verbose_name = "Professor Substituto"
        verbose_name_plural = "Professor Substituto"

    def __str__(self):
        return self.inicio.strftime('%d/%m/%Y')
