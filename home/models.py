from django.db import models
from django.conf import settings

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    componente_curricular = models.TextField(max_length=500,verbose_name = "Componente Curricular")
    substituto = models.BooleanField(default=False)


    class Meta:
        db_table = 'professor'
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome


class Componente_Curricular(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'componente_curricular'
        verbose_name = "Componente Curricular"
        verbose_name_plural = "Componente Curricular"

    def __str__(self):
        return self.nome

class Justificativa(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'justificativa'
        verbose_name = "Justificativa"
        verbose_name_plural = "Justificativa"

    def __str__(self):
        return self.nome

class Segmento(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'segmento'
        verbose_name = "Segmento"
        verbose_name_plural = "Segmento"

    def __str__(self):
        return self.nome

class Periodo(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'periodo'
        verbose_name = "Período"
        verbose_name_plural = "Período"

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=200)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'turma'
        verbose_name = "Turma"
        verbose_name_plural = "Turma"

    def __str__(self):
        return self.nome





