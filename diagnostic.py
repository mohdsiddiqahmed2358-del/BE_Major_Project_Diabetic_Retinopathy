#!/usr/bin/env python
"""
Diagnostic Script for Diabetic Retinopathy System
This script verifies all components are configured correctly and tests data flow
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retinopathy_system.settings')
django.setup()

from django.core.management import call_command
from detection.models import DetectionResult
from images.models import Patient, RetinaImage
from django.db.models import Count
import json

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_database_connection():
    """Test database connectivity"""
    print_header("DATABASE CONNECTION TEST")
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✓ Database connection: OK")
        
        # Test basic queries
        patient_count = Patient.objects.count()
        image_count = RetinaImage.objects.count()
        detection_count = DetectionResult.objects.count()
        
        print(f"  • Patients: {patient_count}")
        print(f"  • Retina Images: {image_count}")
        print(f"  • Detections: {detection_count}")
        return True
    except Exception as e:
        print(f"✗ Database connection FAILED: {e}")
        return False

def test_detection_data():
    """Test detection data variety"""
    print_header("DETECTION DATA VARIETY TEST")
    
    try:
        detections = DetectionResult.objects.filter(
            status='completed'
        ).order_by('detection_date')
        
        if not detections.exists():
            print("⚠ No completed detections found")
            print("  Tip: Upload images and run detection to generate test data")
            return False
        
        print(f"✓ Total detections: {detections.count()}\n")
        
        # Analyze data variance
        ma_counts = [d.microaneurysms_count for d in detections]
        confidence_scores = [d.confidence_score for d in detections]
        lesion_areas = [d.lesion_area for d in detections]
        
        print("Microaneurysm Counts:")
        print(f"  • Range: {min(ma_counts)} - {max(ma_counts)}")
        print(f"  • Unique values: {len(set(ma_counts))}")
        print(f"  • Variance: {'✓ GOOD' if len(set(ma_counts)) > 1 else '✗ ALL SAME'}\n")
        
        print("Confidence Scores (0-1):")
        print(f"  • Range: {min(confidence_scores):.2f} - {max(confidence_scores):.2f}")
        print(f"  • Unique values: {len(set([round(c, 2) for c in confidence_scores]))}")
        print(f"  • Variance: {'✓ GOOD' if len(set([round(c, 2) for c in confidence_scores])) > 1 else '✗ ALL SAME'}\n")
        
        print("Lesion Areas (px²):")
        print(f"  • Range: {min(lesion_areas):.2f} - {max(lesion_areas):.2f}")
        print(f"  • Unique values: {len(set([round(a, 2) for a in lesion_areas]))}")
        print(f"  • Variance: {'✓ GOOD' if len(set([round(a, 2) for a in lesion_areas])) > 1 else '✗ ALL SAME'}\n")
        
        # Show detailed breakdown by patient
        print("Detections by Patient:")
        for patient in Patient.objects.filter(retina_images__detection_result__isnull=False).distinct():
            patient_detections = detections.filter(retina_image__patient=patient)
            if patient_detections.exists():
                print(f"\n  {patient.first_name} {patient.last_name} (ID: {patient.pk})")
                print(f"    Detections: {patient_detections.count()}")
                for d in patient_detections:
                    print(f"      • {d.detection_date.strftime('%b %d %H:%M')} - MA: {d.microaneurysms_count:3d}, Conf: {d.confidence_score*100:5.1f}%, Area: {d.lesion_area:8.2f}")
        
        return True
    except Exception as e:
        print(f"✗ Detection data test FAILED: {e}")
        return False

def test_api_response():
    """Test API response format"""
    print_header("API RESPONSE TEST")
    
    try:
        patient = Patient.objects.filter(retina_images__detection_result__isnull=False).first()
        
        if not patient:
            print("⚠ No patients with detections found")
            return False
        
        detections = list(DetectionResult.objects.filter(
            retina_image__patient=patient,
            status='completed'
        ).order_by('detection_date'))
        
        # Simulate API response
        data = {
            'dates': [d.detection_date.strftime('%b %d, %H:%M') for d in detections],
            'ma_counts': [d.microaneurysms_count for d in detections],
            'lesion_areas': [round(float(d.lesion_area), 2) for d in detections],
            'confidence_scores': [round(float(d.confidence_score) * 100, 2) for d in detections],
            'total_detections': len(detections)
        }
        
        print(f"✓ API Response for {patient.first_name} {patient.last_name}:\n")
        print(json.dumps(data, indent=2))
        
        # Validate data structure
        if len(data['dates']) != len(data['ma_counts']):
            print("\n✗ ERROR: Mismatched array lengths!")
            return False
        
        print(f"\n✓ Data structure valid")
        print(f"✓ All arrays have {len(data['dates'])} elements")
        
        return True
    except Exception as e:
        print(f"✗ API response test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test template configuration"""
    print_header("TEMPLATE CONFIGURATION TEST")
    
    try:
        from django.template import loader
        
        templates_to_test = [
            'tracking/progress.html',
            'tracking/progress_enhanced.html',
            'detection/result.html',
            'images/image_detail.html',
        ]
        
        for template_name in templates_to_test:
            try:
                loader.get_template(template_name)
                print(f"✓ {template_name}")
            except Exception as e:
                print(f"✗ {template_name}: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Template test FAILED: {e}")
        return False

def test_static_files():
    """Test static files collection"""
    print_header("STATIC FILES TEST")
    
    try:
        import os
        static_root = 'staticfiles'
        
        if os.path.exists(static_root):
            file_count = sum([len(files) for _, _, files in os.walk(static_root)])
            print(f"✓ Static files directory exists")
            print(f"✓ Total static files: {file_count}")
            
            # Check for Chart.js
            import glob
            charts = glob.glob(f'{static_root}/**/chart.js', recursive=True)
            if charts:
                print(f"✓ Chart.js found: {charts[0]}")
            else:
                print("⚠ Chart.js not found - run: python manage.py collectstatic")
            
            return True
        else:
            print("⚠ Static files directory not found")
            print("  Run: python manage.py collectstatic")
            return False
    except Exception as e:
        print(f"✗ Static files test FAILED: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("\n")
    print("█" * 60)
    print("█  DIABETIC RETINOPATHY SYSTEM - DIAGNOSTIC REPORT")
    print("█" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Detection Data Variety", test_detection_data),
        ("API Response Format", test_api_response),
        ("Template Configuration", test_templates),
        ("Static Files", test_static_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}  {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All systems operational!")
        print("\nCharts should now display correctly with:")
        print("  • Unique timestamps for each detection")
        print("  • Varying MA counts, confidence, and lesion areas")
        print("  • Proper Chart.js rendering on /tracking/progress/")
    else:
        print("\n⚠ Some tests failed - see details above")
        print("\nCommon fixes:")
        print("  1. Run migrations: python manage.py migrate")
        print("  2. Collect static files: python manage.py collectstatic")
        print("  3. Create test data with detection uploads")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
