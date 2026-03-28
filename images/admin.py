from django.contrib import admin
from .models import Patient, RetinaImage

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'first_name', 'last_name', 'gender', 'created_by', 'created_at']
    list_filter = ['gender', 'created_at', 'created_by']
    search_fields = ['patient_id', 'first_name', 'last_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Patient Information', {'fields': ('patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender')}),
        ('Contact & History', {'fields': ('contact_info', 'medical_history')}),
        ('Metadata', {'fields': ('created_by', 'created_at')}),
    )

@admin.register(RetinaImage)
class RetinaImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'image_type', 'image_format', 'uploaded_by', 'upload_date']
    list_filter = ['image_type', 'image_format', 'upload_date', 'uploaded_by']
    search_fields = ['patient__patient_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['upload_date']
    fieldsets = (
        ('Image Info', {'fields': ('patient', 'original_image', 'image_format', 'image_type')}),
        ('Metadata', {'fields': ('uploaded_by', 'upload_date', 'notes')}),
    )
