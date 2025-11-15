from django.db import models
from django.conf import settings


class Sala(models.Model):
    nome = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"

    def __str__(self):
        return self.nome


class Cuidador(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    profissao = models.CharField(max_length=200 , verbose_name="Profissão")

    class Meta:
        verbose_name = "Cuidador"
        verbose_name_plural = "Cuidadores"

    def __str__(self):
        return self.nome


class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    profissao = models.CharField(max_length=200, verbose_name="Profissão")
    local_trabalho = models.CharField(max_length=100, null=True, blank=True)
    auth_user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='responsaveis',
    verbose_name="Usuário",
    null=True,
    blank=True
    )
    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"



    def __str__(self):
        return self.nome



class Crianca(models.Model):
    SIM_OU_NAO = [
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    AVOS_OU_PAIS_OU_TIOS = [
        ("avós", "avós"),
        ("Pais","Pais"),
        ("Outros", "Outros"),
    ]

    SALA1_OU_SALA2 = [
        ("sala 1", "sala 1"),
        ("sala 2", "sala 2"),
    ]
    
    nome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    rua = models.CharField(max_length=200)
    num = models.IntegerField(verbose_name="Num")
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=200)
    mora_com_quem = models.CharField(max_length=200,  choices=AVOS_OU_PAIS_OU_TIOS, verbose_name="Mora com quem?", blank = False)
    tem_irmaos = models.CharField(max_length=3, choices=SIM_OU_NAO, verbose_name="Tem irmãos?")
    prob_saude = models.CharField(max_length=200, choices=SIM_OU_NAO, verbose_name="prob saúde")
    medic_continuo = models.CharField(max_length=200,  choices=SIM_OU_NAO, verbose_name = "Medic continuo?")
    medic_qual = models.CharField(max_length=200,verbose_name="Medic qual?")
    tem_alergias = models.CharField(max_length=200,  choices=SIM_OU_NAO,verbose_name="tem_alergias?")
    aler_qual = models.CharField(max_length=200, verbose_name="aler_qual?")
    responsaveis = models.ManyToManyField(Responsavel, blank=True)  # Relacionamento M:N


    class Meta:
        verbose_name = "Criança"
        verbose_name_plural = "Crianças"

    def __str__(self):
        return self.nome



class Registro_Diario(models.Model):
    NADA_OU_POUCO_OU_TUDO = [
        ('nada', 'nada'),
        ('pouco', 'pouco'),
        ('tudo', 'tudo')
    ]

    ANO_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ]
   
    SIM_OU_NAO = [
        ('sim', 'Sim'),
        ('não', 'Não'),
    ]

    TRANQUILO_OU_AGITADO_NAODORMIU = [
        ("tranquilo", "tranquilo"),
        ("agitado", "agitado"),
        ("não dormiu", "não dormiu"),
    ]

    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, related_name='registros', verbose_name="Criança")
    cuidador = models.ForeignKey(Cuidador, on_delete=models.SET_NULL, null=True, related_name='registros')
    data = models.DateField()
    cafe = models.CharField(max_length=100, verbose_name="Café", choices=NADA_OU_POUCO_OU_TUDO)
    alm = models.CharField(max_length=100, null=True, blank=True, verbose_name="Almoço", choices=NADA_OU_POUCO_OU_TUDO)
    col = models.CharField(max_length=100, verbose_name = "Colação", choices=NADA_OU_POUCO_OU_TUDO)
    jnt = models.CharField(max_length=100, verbose_name = "Janta", choices=NADA_OU_POUCO_OU_TUDO)
    ev_L = models.CharField(max_length=1, choices=ANO_CHOICES, verbose_name="Ev.Liquida")
    ev_P = models.CharField(max_length=1, choices=ANO_CHOICES, verbose_name="Ev.Pastosa")
    bnh = models.CharField(max_length=100, verbose_name = "Banho", choices=SIM_OU_NAO)
    sono = models.CharField(max_length=100, choices=TRANQUILO_OU_AGITADO_NAODORMIU)
    obs = models.TextField(max_length=25,verbose_name = "observações")   

    class Meta:
        verbose_name = "Registro Diário"
        verbose_name_plural = "Registro Diário"
    def __str__(self):
        return f"Registro de {self.crianca.nome} em {self.data}"


## Novos Modesl

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    componente_curricular = models.TextField(max_length=500,verbose_name = "Componente Curricular")
    substituto = models.BooleanField(default=False)


    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome


class Componente_Curricular(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Componente Curricular"
        verbose_name_plural = "Componente Curricular"

    def __str__(self):
        return self.nome

class Justificativa(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Justificativa"
        verbose_name_plural = "Justificativa"

    def __str__(self):
        return self.nome

class Segmento(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Segmento"
        verbose_name_plural = "Segmento"

    def __str__(self):
        return self.nome

class Periodo(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Período"
        verbose_name_plural = "Período"

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=200)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turma"

    def __str__(self):
        return self.nome





