from django.db import models
from django.conf import settings
from images.models import Patient

class Report(models.Model):
    REPORT_FORMATS = (
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    report_format = models.CharField(max_length=10, choices=REPORT_FORMATS, default='PDF')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    generated_date = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='reports/')
    parameters = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.report_type} - {self.patient.patient_id}"