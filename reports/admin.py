from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'patient', 'report_format', 'generated_by', 'generated_date']
    list_filter = ['report_type', 'report_format', 'generated_date', 'generated_by']
    search_fields = ['patient__patient_id', 'patient__first_name', 'report_type']
    readonly_fields = ['generated_date']
    fieldsets = (
        ('Report Info', {'fields': ('patient', 'report_type', 'report_format')}),
        ('Content', {'fields': ('report_file', 'parameters')}),
        ('Metadata', {'fields': ('generated_by', 'generated_date')}),
    )
