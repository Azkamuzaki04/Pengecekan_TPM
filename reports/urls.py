from django.urls import path
from .views import export_excel, report_list
urlpatterns = [path("", report_list, name="reports"), path("export/excel/", export_excel, name="reports_excel"), path("export/csv/", export_excel, name="reports_csv")]
