from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView



class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        # Rótulos no eixo X
        return ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho"]

    def get_providers(self):
        # Títulos dos conjuntos de dados (linhas)
        return ["Central", "Leste", "Oeste"]

    def get_data(self):
        # Dados de cada linha
        return [
            [75, 44, 92, 11, 44, 95, 35],
            [41, 92, 18, 3, 73, 87, 92],
            [87, 21, 94, 3, 90, 13, 65]
        ]
line_chart = TemplateView.as_view(template_name='home/line_chart.html')
line_chart_json = LineChartJSONView.as_view()
