from django.urls import path
from .views import CheckBrokenLinks, AnalyzeSpreadsheet

urlpatterns = [
    path('check-broken-links/', CheckBrokenLinks.as_view(), name='check_broken_links'),
    path('analyze-spreadsheet/', AnalyzeSpreadsheet.as_view(), name='analyze_spreadsheet'),
]
