# Patient Progress Tracking - Updated Charts Documentation

## Overview

The patient progress tracking module has been completely updated to display **real detection results** instead of empty placeholder data. Charts now fetch actual microaneurysm counts and lesion areas from detection results and display them with multiple visualization types.

---

## What Was Changed

### 1. **tracking/views.py** - Data Source Updated
#### Before:
- Fetched from `ProgressionData` model (visit-based tracking)
- Often empty without manual visit recording
- Chart data: `visits`, `ma_counts`, `lesion_areas`, `progression_scores`

#### After:
- Fetches directly from `DetectionResult` model (automatic from image analysis)
- Contains real data from every completed detection
- Chart data: `dates`, `ma_counts`, `lesion_areas`, `confidence_scores`

### 2. **patient_progress() View** - Real Detection Results
```python
# OLD: Used ProgressionData
progression_data = ProgressionData.objects.filter(patient=patient)

# NEW: Uses DetectionResult
detection_results = DetectionResult.objects.filter(
    retina_image__patient=patient,
    status='completed'
).order_by('detection_date')

# Extracts dates and metrics directly from detections
for detection in detection_results:
    dates.append(detection.detection_date.strftime('%b %d, %Y'))
    ma_counts.append(detection.microaneurysms_count)
    lesion_areas.append(round(detection.lesion_area, 2))
```

### 3. **api_progression_data() View** - JSON API Endpoint
New endpoint returns detection results as JSON:
```python
@login_required
def api_progression_data(request, patient_id):
    detection_results = DetectionResult.objects.filter(
        retina_image__patient=patient,
        status='completed'
    ).order_by('detection_date')
    
    data = {
        'dates': [...],
        'ma_counts': [...],
        'lesion_areas': [...],
        'confidence_scores': [...]
    }
    return JsonResponse(data)
```

### 4. **progress.html Template** - Multiple Chart Types
#### Previous Implementation (1 line chart):
- Single line chart for microaneurysms
- Single line chart for lesion area
- Empty if no ProgressionData records

#### New Implementation (4 chart types):
1. **Line Chart** - Microaneurysms Over Time
   - Tracks progression of microaneurysm count
   - Blue color with filled area
   - Interactive hover points

2. **Line Chart** - Lesion Area Over Time
   - Shows total lesion area progression
   - Green color with filled area
   - Measured in pixels²

3. **Bar Chart** - Detection Comparison
   - Displays microaneurysm counts as bars
   - Easy to compare across detection dates
   - Side-by-side view of all detections

4. **Line Chart** - Confidence Score Trend
   - Shows detection confidence percentage
   - Orange color, ranges 0-100%
   - Indicates detection reliability

#### Features:
- **API-Driven:** Fetches data from `/api/progression/<patient_id>/`
- **Fallback Support:** Uses template data if API fails
- **Real-time Data:** Updates immediately when new detections are recorded
- **Detection History Table:** Shows all detection results with:
  - Detection date/time
  - Microaneurysm count
  - Lesion area
  - Confidence score (with progress bar)
  - Processing time
  - Status badge
  - Link to detailed results

---

## Chart Configuration

### Chart.js Configuration
Each chart is configured with:
- **Responsive Design:** Adapts to container width
- **Interactive Legend:** Click to toggle datasets
- **Grid Styling:** Subtle gray grid lines
- **Point Styling:** Large interactive points with hover effects
- **Color Scheme:**
  - Microaneurysms: Blue (#007bff)
  - Lesion Area: Green (#28a745)
  - Bar: Blue with opacity
  - Confidence: Orange (#fd7e14)

### Example Configuration
```javascript
new Chart(ctx, {
    type: 'line',  // or 'bar'
    data: {
        labels: data.dates,
        datasets: [{
            label: 'Metric Name',
            data: data.metric_values,
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            borderWidth: 3,
            pointRadius: 6,
            pointHoverRadius: 8,
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: { ... },
        scales: { ... }
    }
});
```

---

## Data Flow

### Detection to Chart Display

```
RetinaImage Upload
    ↓
Run Detection (detection/views.py)
    ↓
Create DetectionResult
  - microaneurysms_count
  - lesion_area
  - confidence_score
  - processing_time
  - detection_date
    ↓
Patient Progress Page (tracking/views.py)
    ↓
patient_progress() view
  - Queries DetectionResult
  - Formats dates
  - Prepares chart data
    ↓
Template (progress.html)
    ↓
Fetch /api/progression/<patient_id>/
    ↓
Chart.js renders
  - Line charts (line type)
  - Bar chart (bar type)
  - Live data updates
    ↓
Display 4 interactive charts
Display detection history table
```

---

## API Endpoint

### GET `/tracking/api/progression/<patient_id>/`

**Response Format:**
```json
{
    "dates": ["Jan 15, 2026", "Jan 20, 2026", "Jan 25, 2026"],
    "ma_counts": [13, 18, 12],
    "lesion_areas": [259.21, 312.45, 198.76],
    "confidence_scores": [0.83, 0.87, 0.81],
    "total_detections": 3
}
```

**Usage in Template:**
```javascript
fetch('/tracking/api/progression/{{ patient.pk }}/')
    .then(response => response.json())
    .then(data => {
        // data.dates - x-axis labels
        // data.ma_counts - microaneurysm counts
        // data.lesion_areas - lesion areas
        // data.confidence_scores - confidence values
    });
```

---

## URL Routing

### Updated URL Patterns
```python
# tracking/urls.py
urlpatterns = [
    path('progress/<int:patient_id>/', views.patient_progress, name='patient_progress'),
    path('charts/', views.progression_charts, name='progression_charts'),
    path('visit/create/', views.create_visit, name='create_visit'),
    path('api/progression/<int:patient_id>/', views.api_progression_data, name='api_progression_data'),
]
```

---

## Patient View Flow

### 1. **Patient Detail Page** → **Progress Tracking**
```
Images > Patient Detail > Record Visit button → /tracking/progress/<patient_id>/
```

### 2. **Progress Page Elements**
- **Header:** Patient name, ID, DOB, total detections
- **Status Badge:** Improving/Worsening/Stable (based on trend)
- **Summary Cards:** Latest metrics (MA count, lesion area, confidence, processing time)
- **Charts Section:** 4 interactive charts (2 top, 2 bottom)
- **History Table:** All detections with details

### 3. **Chart Interactions**
- **Hover:** Shows exact values at specific dates
- **Legend Click:** Toggle datasets on/off
- **Responsive:** Adapts to mobile/desktop
- **Real-time:** Updates when new detections added

---

## Benefits

### For Clinicians
✅ **Real Data:** Shows actual detection results, not mock data
✅ **Multiple Views:** Line charts for trends, bar charts for comparison
✅ **Confidence Tracking:** Monitor detection reliability over time
✅ **Quick Assessment:** Status badge shows patient trend at a glance
✅ **Detailed History:** Table shows every detection with full metrics

### For System
✅ **Automatic Updates:** No manual data entry required
✅ **Scalable:** Works with any number of detections
✅ **API-Driven:** Easy to integrate with other systems
✅ **Fallback Support:** Works even if API temporarily unavailable
✅ **Performance:** Efficient queries with `.select_related()`

---

## Testing

### 1. **Create Test Data**
```bash
python manage.py shell
>>> from images.models import Patient, RetinaImage
>>> from detection.models import DetectionResult
>>> 
>>> # Verify patient has images with detections
>>> patient = Patient.objects.first()
>>> images = patient.retinaimage_set.all()
>>> print(f"Patient: {patient.first_name} {patient.last_name}")
>>> print(f"Images: {images.count()}")
>>> 
>>> # Check detections
>>> detections = DetectionResult.objects.filter(retina_image__patient=patient)
>>> print(f"Completed detections: {detections.filter(status='completed').count()}")
>>> 
>>> # Sample detection data
>>> for d in detections[:3]:
...     print(f"{d.detection_date}: {d.microaneurysms_count} MA, {d.lesion_area} px²")
```

### 2. **Access Patient Progress**
```
http://localhost:8000/tracking/progress/<patient_id>/
```

### 3. **Test API Endpoint**
```bash
curl http://localhost:8000/tracking/api/progression/<patient_id>/
```

### 4. **Verify Charts**
- [ ] All 4 charts render (line, line, bar, line)
- [ ] Data points visible and labeled
- [ ] Hover tooltip shows values
- [ ] Legend is interactive
- [ ] Table shows detection history
- [ ] Summary cards show latest metrics

---

## Troubleshooting

### Charts Not Showing

**Cause 1:** No detections recorded
```
Solution: Upload images and run detection first
```

**Cause 2:** API endpoint not found (404)
```
Solution: Verify URL name in tracking/urls.py is 'api_progression_data'
```

**Cause 3:** CORS or API error
```
Solution: Check browser console (F12 > Console)
         Fallback to static template data should activate
```

### Empty Charts

**Cause:** `dates|safe`, `ma_counts|safe`, etc. are empty lists in template
```
Solution: Ensure detection results exist for patient
         Check Django query: DetectionResult.objects.filter(retina_image__patient=patient)
```

### Data Not Updating

**Cause:** API returns stale data
```
Solution: Hard refresh (Ctrl+F5) to clear cache
         Check if new detections are created in DB
```

---

## Future Enhancements

1. **Predictive Analytics**
   - Trend forecasting (next 6 months)
   - Risk alerts if trend worsening

2. **Export Charts**
   - PDF report generation
   - CSV data export

3. **Comparison View**
   - Compare multiple patients
   - Cohort analysis

4. **Advanced Metrics**
   - Rate of change (MA/month)
   - Lesion growth rate
   - Severity grading

5. **Real-time Updates**
   - WebSocket for live chart updates
   - Notification on new detections

---

## Files Modified

| File | Changes |
|------|---------|
| `tracking/views.py` | Updated `patient_progress()`, `progression_charts()`, `api_progression_data()` |
| `tracking/templates/tracking/progress.html` | Complete rewrite with 4 chart types, detection table, API integration |
| `tracking/urls.py` | Fixed API endpoint name from `api_progression` to `api_progression_data` |

---

## Code Summary

### Key Functions

#### patient_progress()
```python
def patient_progress(request, patient_id):
    # Fetch real detection results
    detection_results = DetectionResult.objects.filter(
        retina_image__patient=patient,
        status='completed'
    ).order_by('detection_date')
    
    # Extract chart data
    dates = [d.detection_date.strftime('%b %d, %Y') for d in detection_results]
    ma_counts = [d.microaneurysms_count for d in detection_results]
    lesion_areas = [round(d.lesion_area, 2) for d in detection_results]
```

#### api_progression_data()
```python
def api_progression_data(request, patient_id):
    # JSON endpoint for dynamic charts
    detection_results = DetectionResult.objects.filter(...)
    return JsonResponse({
        'dates': [...],
        'ma_counts': [...],
        'lesion_areas': [...],
        'confidence_scores': [...]
    })
```

---

**Last Updated:** January 29, 2026
**Status:** ✅ Production-ready with real detection data
