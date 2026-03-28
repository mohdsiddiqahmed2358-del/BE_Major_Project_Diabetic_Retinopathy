from django.contrib import admin
from .models import PatientVisit, ProgressionData, TreatmentPlan

@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['visit_number', 'patient', 'visit_date', 'visit_type', 'created_by']
    list_filter = ['visit_type', 'visit_date', 'created_by']
    search_fields = ['patient__patient_id', 'patient__first_name', 'notes']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Visit Info', {'fields': ('patient', 'visit_number', 'visit_type', 'visit_date')}),
        ('Details', {'fields': ('notes',)}),
        ('Metadata', {'fields': ('created_by', 'created_at')}),
    )

@admin.register(ProgressionData)
class ProgressionDataAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit', 'total_microaneurysms', 'progression_score', 'recorded_date']
    list_filter = ['recorded_date', 'patient', 'progression_score']
    search_fields = ['patient__patient_id', 'patient__first_name']
    readonly_fields = ['recorded_date']

@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'patient', 'start_date', 'end_date', 'is_active', 'created_by']
    list_filter = ['is_active', 'start_date', 'created_by']
    search_fields = ['patient__patient_id', 'plan_name', 'description']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Plan Info', {'fields': ('patient', 'plan_name', 'description')}),
        ('Dates', {'fields': ('start_date', 'end_date')}),
        ('Status', {'fields': ('is_active',)}),
        ('Metadata', {'fields': ('created_by', 'created_at')}),
    )
