from django.contrib import admin
from django.urls import path
from home.views import line_chart, line_chart_json
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('class-board/', admin.site.urls),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
