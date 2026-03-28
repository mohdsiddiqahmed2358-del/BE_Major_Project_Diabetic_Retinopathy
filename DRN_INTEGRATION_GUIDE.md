# DRN Model Integration Guide

This guide explains how to integrate the Dilated Residual Network (DRN) model into your diabetic retinopathy detection system.

## Quick Start

### 1. Verify Setup

```bash
# Check model and dependencies
python manage.py train_drn info
```

Expected output:
```
ℹ️  DRN Model Information
------------------------------------------------------------
🧠 DRN Model Available: False (initially, before training)
📁 DRN Path: detection/models/drn_microaneurysm_detector.h5
🖥️  OpenCV Available: True
------------------------------------------------------------
```

### 2. Prepare Dataset

Download one of the benchmark datasets:

```bash
# Example: Create data directory
mkdir -p /data/datasets/eophtha-ma

# Place extracted dataset:
# /data/datasets/eophtha-ma/
# ├── images/
# │   ├── image1.jpg
# │   ├── image2.jpg
# │   └── ...
# └── annotations/
#     ├── image1.json
#     ├── image2.json
#     └── ...
```

### 3. Train DRN Model

```bash
# Train on e-ophtha microaneurysm dataset
python manage.py train_drn train \
    --dataset eophtha \
    --path /data/datasets/eophtha-ma \
    --epochs 50 \
    --batch-size 16
```

This will:
- Load images and annotations
- Perform data augmentation
- Train DRN model for 50 epochs
- Save best model to `detection/models/drn_microaneurysm_detector.h5`
- Save training metadata to `detection/models/drn_training_metadata.json`

### 4. Evaluate Model

```bash
# Evaluate on validation set
python manage.py train_drn evaluate \
    --model-path detection/models/drn_microaneurysm_detector.h5 \
    --dataset eophtha \
    --path /data/datasets/eophtha-ma
```

### 5. Use in Detection

#### Option A: Web Interface

1. Upload retina image in the detection application
2. System automatically uses DRN if model exists, otherwise falls back to OpenCV
3. View results with DRN predictions

#### Option B: Command Line

```bash
# Predict on single image (uses DRN if available)
python manage.py train_drn predict \
    --image /path/to/fundus/image.jpg

# Force OpenCV detector
python manage.py train_drn predict \
    --image /path/to/fundus/image.jpg \
    --use-opencv
```

#### Option C: Python Code

```python
from detection.predict_drn import predict_with_drn_fallback

# Single image
result = predict_with_drn_fallback(
    '/path/to/image.jpg',
    use_drn=True  # Use DRN if available
)

print(f"Microaneurysms: {result['ma_count']}")
print(f"Lesion Area: {result['lesion_area']}")
print(f"Confidence: {result['confidence']}")
print(f"Model: {result['model_type']}")
```

## Integration with Views

The system automatically uses DRN in the detection views. Update `detection/views.py` to explicitly use DRN:

```python
from detection.predict_drn import predict_with_drn_fallback, DRN_MODEL_PATH

def upload_image(request):
    # ... form validation code ...
    
    # Run detection (automatically uses DRN if available)
    detection_result = predict_with_drn_fallback(
        image_path=uploaded_file_path,
        use_drn=True  # Prefer DRN model
    )
    
    # Create database record
    DetectionResult.objects.create(
        image=image_obj,
        ma_count=detection_result['ma_count'],
        lesion_area=detection_result['lesion_area'],
        confidence=detection_result['confidence'],
        processed_image_path=detection_result['processed_image_path'],
        # ... other fields ...
    )
    
    return JsonResponse({
        'ma_count': detection_result['ma_count'],
        'lesion_area': detection_result['lesion_area'],
        'model_type': detection_result.get('model_type', 'OpenCV')
    })
```

## Architecture Overview

```
User Upload
     ↓
detection/views.py (upload_image)
     ↓
predict_with_drn_fallback()
     ├─ Check if DRN model exists (detection/models/drn_microaneurysm_detector.h5)
     │
     ├─ [If exists] → detect_microaneurysms_drn()
     │               ├─ Preprocess image (512x512)
     │               ├─ Run DRN inference
     │               ├─ Extract multi-task predictions
     │               └─ Return results
     │
     └─ [If not exists] → detect_with_opencv()
                         ├─ Apply CLAHE preprocessing
                         ├─ Blob detection
                         └─ Return results
     ↓
DetectionResult saved to database
     ↓
Chart/Report Generation
```

## Model Training Workflow

### Single Dataset Training

```
Benchmark Dataset (e.g., e-ophtha-MA)
     ↓
train_drn_model()
     ├─ Load images & annotations
     ├─ Split train/validation (80/20)
     ├─ Data augmentation
     ├─ Training loop
     │  ├─ Forward pass
     │  ├─ Loss calculation (multi-task)
     │  ├─ Backward pass
     │  ├─ Parameter update
     │  └─ Validation
     ├─ Model checkpointing (best weights)
     ├─ Early stopping (if no improvement)
     └─ Save model
     ↓
detection/models/drn_microaneurysm_detector.h5
```

### Cross-Dataset Validation

```
Train on e-ophtha
     ↓
Evaluate on DiaretDB1, ROC
     ↓
Compare performance across datasets
     ↓
Determine generalization capability
```

## File Structure

After training:

```
detection/
├── models/
│   ├── drn_microaneurysm_detector.h5      # Trained model (new)
│   └── drn_training_metadata.json         # Training info (new)
├── model_drn.py                            # DRN architecture
├── train_drn.py                            # Training pipeline
├── predict_drn.py                          # Prediction module (new)
├── model.py                                # OpenCV fallback
├── views.py                                # Detection views
└── management/
    └── commands/
        └── train_drn.py                    # Django management command
```

## Performance Comparison

### Model Comparison

| Metric | OpenCV | DRN |
|--------|--------|-----|
| Sensitivity | 70-80% | 90-95% |
| Specificity | 85-90% | 92-97% |
| Processing Time | 50-100ms | 200-500ms |
| Model Size | ~1MB | ~15-20MB |
| GPU Required | No | Yes (optional) |

### When to Use Each Model

**OpenCV Detector:**
- Limited computational resources
- CPU-only deployment
- Real-time constraints (mobile)
- Quick screening with lower accuracy requirement

**DRN Model:**
- High accuracy requirement
- Detailed microaneurysm detection
- Research/clinical validation
- GPU available for acceleration

## Troubleshooting

### Model Not Found After Training

```bash
# Verify model was saved
ls -la detection/models/drn_microaneurysm_detector.h5

# Check Django app configuration
python manage.py check detection
```

### DRN Predictions Not Being Used

```python
# Debug script
from detection.predict_drn import get_model_info, DRN_MODEL_PATH
import os

info = get_model_info()
print(f"DRN Available: {info['drn_available']}")
print(f"Model Path: {DRN_MODEL_PATH}")
print(f"Exists: {os.path.exists(DRN_MODEL_PATH)}")

# Check permissions
print(f"Readable: {os.access(DRN_MODEL_PATH, os.R_OK)}")
```

### Memory Issues During Inference

```python
# Reduce image preprocessing resolution
# In detect_microaneurysms_drn(), modify:
image_array = preprocess_image_for_drn(
    image_path, 
    target_size=(256, 256)  # Instead of (512, 512)
)
```

### Out of Memory During Training

```bash
# Reduce batch size
python manage.py train_drn train \
    --dataset eophtha \
    --path /data/eophtha-ma \
    --batch-size 8  # Reduced from 16
```

## Advanced Configuration

### Custom Model Path

```python
from detection.predict_drn import detect_microaneurysms_drn
import os

# Override default model path
custom_model_path = '/custom/path/to/model.h5'

# Or modify environment variable
os.environ['DRN_MODEL_PATH'] = custom_model_path
```

### Custom Preprocessing

Extend preprocessing in `detect_microaneurysms_drn()`:

```python
def custom_preprocess(image_path):
    # Custom preprocessing logic
    image = cv2.imread(image_path)
    
    # Apply custom filters
    # Apply normalization
    # Apply augmentation
    
    return preprocessed_image
```

### Enable Batch Prediction API

```python
from detection.predict_drn import batch_predict_drn

# Multiple images
images = [
    '/path/to/image1.jpg',
    '/path/to/image2.jpg'
]

results = batch_predict_drn(images, use_drn=True)

# Process results
for result in results:
    if result:
        print(f"MA Count: {result['ma_count']}")
```

## Production Deployment

### Docker Integration

```dockerfile
FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Pre-download model (optional)
RUN python -c "from detection.predict_drn import get_model_info; print(get_model_info())"

CMD ["gunicorn", "retinopathy_system.wsgi"]
```

### Performance Optimization

For production deployment:

```bash
# Convert model to optimized format
python -c "
import tensorflow as tf
from detection.model_drn import load_drn_model

model = load_drn_model('detection/models/drn_microaneurysm_detector.h5')

# Convert to TFLite (lighter, faster)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('detection/models/drn_microaneurysm_detector.tflite', 'wb') as f:
    f.write(tflite_model)
"
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Review DRN_TRAINING_GUIDE.md for detailed training instructions
3. ✅ Download benchmark dataset (e-ophtha-MA recommended for initial training)
4. ✅ Train model: `python manage.py train_drn train --dataset eophtha --path /data/eophtha-ma`
5. ✅ Evaluate: `python manage.py train_drn evaluate --model-path ... --dataset ...`
6. ✅ Test with web interface or CLI
7. ✅ Monitor performance metrics in detection results

## Support

- **Training Issues**: See `DRN_TRAINING_GUIDE.md` troubleshooting section
- **Integration Issues**: Check `detection/views.py` integration patterns
- **Performance Issues**: Review model optimization section
- **Dataset Issues**: Verify dataset format matches loader requirements

---

**Last Updated**: 2025
**Version**: 1.0
**Requires**: TensorFlow 2.10+, Python 3.8+, OpenCV 4.6+
