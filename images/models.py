from django.db import models
from django.conf import settings

class Patient(models.Model):
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    contact_info = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"

class RetinaImage(models.Model):
    IMAGE_FORMATS = (
        ('JPEG', 'JPEG'),
        ('PNG', 'PNG'),
        ('TIFF', 'TIFF'),
    )
    IMAGE_TYPES = (
        ('FUNDUS', 'Fundus'),
        ('NON_FUNDUS', 'Non-Fundus'),
        ('UNKNOWN', 'Unknown'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='retina_images')
    original_image = models.ImageField(upload_to='retina_images/original/')
    image_format = models.CharField(max_length=10, choices=IMAGE_FORMATS)
    image_type = models.CharField(max_length=12, choices=IMAGE_TYPES, default='UNKNOWN')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"Image {self.id} - {self.patient}"