from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from datetime import datetime
import os
import locale
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from .models import Sala, Cuidador, Responsavel, Crianca, Registro_Diario, Professor, Justificativa, Segmento, Turma, \
    Periodo, Componente_Curricular

# --- Define locale para datas em português ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/Mac
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  # Windows

# --- Filtro por mês no admin ---
class MesFiltro(SimpleListFilter):
    title = 'Mês'
    parameter_name = 'mes'

    def lookups(self, request, model_admin):
        meses = Registro_Diario.objects.dates('data', 'month')
        return [(d.strftime("%Y-%m"), d.strftime("%B/%Y").capitalize()) for d in meses]

    def queryset(self, request, queryset):
        if self.value():
            ano, mes = self.value().split("-")
            return queryset.filter(data__year=ano, data__month=mes)

class FilterLoginGroup(SimpleListFilter):
    title = 'Criança'
    parameter_name = 'crianca'

    def lookups(self, request, model_admin):
        from .models import Crianca  # Ajuste se estiver em outro app
        usuario = request.user
        user_id = usuario.pk
        grupos = usuario.groups.all()
        existe = usuario.groups.filter(name__icontains='Responsaveis').exists()  
        if existe :
            return [(c.id, c.nome) for c in Crianca.objects.filter(responsaveis__auth_user_id=user_id)[0:1]]
        else:
            return [(c.id, c.nome) for c in Crianca.objects.all()]  

    def queryset(self, request, queryset):
        if self.value():
            usuario = request.user
            user_id = usuario.pk
            grupos = usuario.groups.all()
            existe = usuario.groups.filter(name__icontains='Responsaveis').exists()  
            responsaveis_ids = [1, 2, 3, 23]
            if existe :
                return queryset.filter(crianca__responsaveis__auth_user_id=user_id)
                #return queryset.filter(crianca__id=21)
            else: 
                return queryset.filter(crianca__id=self.value())
        return queryset    

# --- Função para rodapé com data e nome do usuário ---
def rodape(canvas, doc):
    canvas.saveState()
    largura, altura = A4

    data_str = datetime.now().strftime("%d de %B de %Y")
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawString(2 * cm, 1.5 * cm, f"Data de emissão: {data_str}")

    nome_usuario = getattr(doc, 'nome_usuario', '')
    if nome_usuario:
        canvas.drawRightString(largura - 2 * cm, 1.5 * cm, f"Emitido por: {nome_usuario}")

    canvas.restoreState()

# --- Função para exportar PDF ---
def exportar_modelo_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    campos = [field.name for field in meta.fields if field.name != 'id']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name_plural}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            leftMargin=3*cm, rightMargin=3*cm,
                            topMargin=3*cm, bottomMargin=3*cm)

    elementos = []

    # --- Cabeçalho com logo e título centralizado ---
    caminho_logo = os.path.join(settings.BASE_DIR, 'home', 'static', 'logo-painel_interativo.jpeg')
    styles = getSampleStyleSheet()

    if os.path.exists(caminho_logo):
        img = Image(caminho_logo, width=3.5*cm, height=2*cm)
    else:
        img = Spacer(3.5*cm, 2*cm)  # Espaço reservado

    titulo = Paragraph(
        f'<b><font size=14 color=blue>{meta.verbose_name_plural.title()}</font></b>',
        ParagraphStyle(name='TituloCentral', alignment=TA_CENTER, fontSize=14)
    )

    cabecalho = Table(
        [[img, titulo]],
        colWidths=[4*cm, 12*cm]
    )
    cabecalho.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elementos.append(cabecalho)
    elementos.append(Spacer(1, 12))

    # --- Quantidade de registros ---
    total_registros = queryset.count()
    estilo_qtd = ParagraphStyle(name='Centro', alignment=TA_CENTER, fontSize=10)
    qtd_paragraph = Paragraph(f"<b>Quantidade de registros: {total_registros}</b>", estilo_qtd)
    elementos.append(qtd_paragraph)
    elementos.append(Spacer(1, 12))

    # --- Tabela de dados ---
    dados = [[campo.title() for campo in campos]]
    for obj in queryset:
        linha = [str(getattr(obj, campo)) for campo in campos]
        dados.append(linha)

    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabela)

    # --- Nome do usuário autenticado ---
    usuario = request.user
    nome_usuario = usuario.get_full_name() or usuario.username if usuario.is_authenticated else ""
    doc.nome_usuario = nome_usuario

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

    return response

exportar_modelo_pdf.short_description = "Exportar como PDF"

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao')
    list_filter = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'profissao', 'local_trabalho', 'auth_user')
    list_filter = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sala', 'data_de_nascimento', 'rua', 'num',
                    'cidade', 'cep', 'mora_com_quem', 'tem_irmaos', 'prob_saude',
                    'medic_continuo', 'medic_qual', 'tem_alergias',
                    'aler_qual')
    list_filter = ('nome', )
    actions = [exportar_modelo_pdf] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            print("DEBUG: Tipo do widget:", type(field.widget))
            field.widget.can_add_related = False  # Remove o botão de "adicionar"
            field.widget.can_change_related = False  # Remove o botão de "editar"
            return field

@admin.register(Registro_Diario)
class Registro_DiarioAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'cuidador', 'data',
                    'cafe', 'alm', 'col', 'jnt',
                    'ev_L', 'ev_P', 'bnh',
                    'sono', 'obs')
    list_filter = (FilterLoginGroup, MesFiltro)
    
    def changelist_view(self, request, extra_context=None):
        # Verifica se há parâmetros de filtro ou busca
        if not request.GET:
            self.message_user(request, "Utilize ao menos um dos filtros para exibir os resultados.", level="info")
            # Substitui o queryset por um vazio
            self.get_queryset = lambda request: self.model.objects.none()
        else:
            usuario = request.user
            user_id = usuario.pk
            grupos = usuario.groups.all()
            for grupo in grupos:
                print(f"Grupo: {grupo.name}")

            existe = usuario.groups.filter(name__icontains='Responsaveis').exists()  
            print(f"Existe: {existe}")

            if existe :
                self.get_queryset = lambda request: self.model.objects.filter(crianca__responsaveis__auth_user_id=user_id)
            else:
                self.get_queryset = lambda request: self.model.objects.all()
            
        return super().changelist_view(request, extra_context=extra_context)
    actions = [exportar_modelo_pdf]

    ## Novos

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome','telefone','componente_curricular','substituto_formatado')
    actions = [exportar_modelo_pdf]

    def substituto_formatado(self, obj):
        return "Sim" if obj.substituto else "Não"

    substituto_formatado.short_description = "Substituto"

@admin.register(Justificativa)
class JustificativaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome','segmento','periodo')
    actions = [exportar_modelo_pdf]

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Componente_Curricular)
class Componente_CurricularAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

    