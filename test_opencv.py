#!/usr/bin/env python
import sys
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retinopathy_system.settings')
django.setup()

def test_imports():
    """Test if all required modules can be imported"""
    modules_to_test = [
        'django',
        'PIL',  # Pillow
        'numpy',
        'matplotlib',
        'pandas',
        'reportlab',
        'openpyxl',
        'django_crispy_forms',
        'decouple',
    ]
    
    print("Testing module imports...")
    for module_name in modules_to_test:
        try:
            if module_name == 'PIL':
                import PIL
                print(f"✅ {module_name} (Pillow)")
            else:
                __import__(module_name)
                print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
    
    print("\nTesting Django apps...")
    try:
        from users.models import CustomUser
        from images.models import Patient, RetinaImage
        from detection.models import DetectionResult
        print("✅ All Django models imported successfully")
    except Exception as e:
        print(f"❌ Django models: {e}")

if __name__ == "__main__":
    test_imports()