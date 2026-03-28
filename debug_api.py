import os, django, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'retinopathy_system.settings'
django.setup()

from detection.models import DetectionResult
from images.models import Patient

# Get patient with ID 2
patient = Patient.objects.filter(pk=2).first()
if patient:
    print(f"Patient: {patient.first_name} {patient.last_name} (ID: {patient.pk})\n")
    
    detection_results = DetectionResult.objects.filter(
        retina_image__patient=patient,
        status='completed'
    ).select_related('retina_image').order_by('detection_date')
    
    print(f"Detections for patient {patient.pk}: {detection_results.count()}\n")
    print("Details:")
    for d in detection_results:
        print(f"  {d.detection_date.strftime('%b %d')} - MA: {d.microaneurysms_count}, Conf: {d.confidence_score:.2f} ({d.confidence_score*100:.2f}%), Area: {d.lesion_area:.2f}")
    
    print("\n\nAPI Response data would be:")
    data = {
        'dates': [d.detection_date.strftime('%b %d, %Y') for d in detection_results],
        'ma_counts': [d.microaneurysms_count for d in detection_results],
        'lesion_areas': [round(float(d.lesion_area), 2) for d in detection_results],
        'confidence_scores': [round(float(d.confidence_score) * 100, 2) for d in detection_results],
        'total_detections': detection_results.count()
    }
    print(json.dumps(data, indent=2))
else:
    print("Patient 2 not found")
