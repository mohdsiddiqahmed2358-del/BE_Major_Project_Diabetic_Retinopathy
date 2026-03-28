from django.db import models
from django.conf import settings
from images.models import Patient
from detection.models import DetectionResult

class PatientVisit(models.Model):
    VISIT_TYPES = (
        ('initial', 'Initial Screening'),
        ('followup', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine', 'Routine Checkup'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField()
    visit_number = models.IntegerField()
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES, default='routine')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-visit_date']
        unique_together = ['patient', 'visit_number']

    def __str__(self):
        return f"Visit {self.visit_number} - {self.patient}"

class ProgressionData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='progression_data')
    visit = models.ForeignKey(PatientVisit, on_delete=models.CASCADE)
    detection_result = models.ForeignKey(DetectionResult, on_delete=models.CASCADE)
    total_microaneurysms = models.IntegerField()
    total_lesion_area = models.FloatField()
    progression_score = models.FloatField(default=0.0)
    recorded_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['visit__visit_date']

    def __str__(self):
        return f"Progression - {self.patient} - Visit {self.visit.visit_number}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_plans')
    plan_name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.plan_name} - {self.patient}"