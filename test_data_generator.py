"""Generate test patients, images and detection results for local testing.
Run with: python test_data_generator.py
"""
import os
import random
import uuid
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retinopathy_system.settings')
import django
django.setup()

from django.conf import settings
from PIL import Image, ImageDraw
from images.models import Patient, RetinaImage
from detection.models import DetectionResult, Microaneurysm
from detection.model import predict_image

MEDIA_ROOT = Path(settings.MEDIA_ROOT)
ORIG_DIR = MEDIA_ROOT / 'retina_images' / 'original'
ORIG_DIR.mkdir(parents=True, exist_ok=True)

def make_dummy_image(path, fundus=True):
    img = Image.new('RGB', (800, 600), (120, 120, 120) if not fundus else (30, 30, 30))
    draw = ImageDraw.Draw(img)
    if fundus:
        # Draw a reddish circular region to simulate fundus
        draw.ellipse((200,100,600,500), fill=(120,30,30))
    img.save(path, quality=85)


def create_test_data(num_patients=2, images_per_patient=3):
    for pidx in range(1, num_patients+1):
        patient, created = Patient.objects.get_or_create(
            patient_id=f"TEST{pidx}",
            defaults={
                'first_name': f'Test{pidx}',
                'last_name': 'User',
                'date_of_birth': '1990-01-01',
                'gender': 'O',
                'created_by_id': 1
            }
        )
        for i in range(images_per_patient):
            fname = f"test_{patient.patient_id}_{uuid.uuid4().hex[:8]}.jpg"
            fpath = ORIG_DIR / fname
            # Alternate fundus / non-fundus
            fundus = (i % 2 == 0)
            make_dummy_image(fpath, fundus=fundus)
            ri = RetinaImage.objects.create(
                patient=patient,
                original_image=f"retina_images/original/{fname}",
                image_format='JPEG',
                uploaded_by_id=1,
                image_type='FUNDUS' if fundus else 'NON_FUNDUS'
            )
            # Run prediction
            try:
                data = predict_image(ri)
                dr = DetectionResult.objects.create(
                    retina_image=ri,
                    processed_image=data.get('processed_image_relative_path') or '',
                    microaneurysms_count=data.get('ma_count', 0),
                    lesion_area=data.get('lesion_area', 0.0),
                    confidence_score=data.get('confidence', 0.0),
                    processing_time=data.get('processing_time', 0.0),
                    status='completed',
                    safe_prediction=data.get('non_fundus', False)
                )
                for ma in data.get('microaneurysms', []):
                    Microaneurysm.objects.create(
                        detection_result=dr,
                        x_coordinate=ma['x'],
                        y_coordinate=ma['y'],
                        diameter=ma['diameter'],
                        confidence=ma.get('confidence', 0.8)
                    )
                print(f"Created detection for {ri}")
            except Exception as e:
                print(f"Prediction failed for {ri}: {e}")

if __name__ == '__main__':
    create_test_data(num_patients=2, images_per_patient=4)
    print('Test data generation complete.')
