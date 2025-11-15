from django.db import models

class Mensagem(models.Model):
    TIPOS_MENSAGEM = [
        ("comunicacao", "Comunicação"),
        ("evento", "Evento"),
        ("observacao", "Observação"),
        ("pedagogicos", "Pedagógicos"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_MENSAGEM, verbose_name="Tipo")
    data = models.DateField()
    descricao = models.TextField(verbose_name="Descrição")
    imagem = models.ImageField(upload_to="images/user")

    turmas = models.ManyToManyField('home.Turma', blank=True)  # Relacionamento M:N
    professores = models.ManyToManyField('home.Professor', blank=True)  # Relacionamento M:N

    class Meta:
        db_table = 'mensagem'
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return self.tipo

