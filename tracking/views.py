from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Max, Min
from django.http import JsonResponse
from images.models import Patient
from detection.models import DetectionResult
from .models import PatientVisit, ProgressionData, TreatmentPlan
from .forms import PatientVisitForm, TreatmentPlanForm

@login_required
def patient_progress(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
    
    # Fetch all detection results for this patient's images, ordered by date
    # Convert to list to support negative indexing in templates
    detection_results = list(DetectionResult.objects.filter(
        retina_image__patient=patient,
        status='completed'
    ).select_related('retina_image').order_by('detection_date'))
    
    # Also fetch progression data for visit-based tracking
    progression_data = ProgressionData.objects.filter(
        patient=patient
    ).select_related('visit', 'detection_result').order_by('visit__visit_date')
    
    treatment_plans = TreatmentPlan.objects.filter(patient=patient, is_active=True)
    
    # Prepare chart data from detection results
    dates = []
    ma_counts = []
    lesion_areas = []
    confidence_scores = []
    
    for detection in detection_results:
        dates.append(detection.detection_date.strftime('%b %d, %H:%M'))
        ma_counts.append(detection.microaneurysms_count)
        lesion_areas.append(round(detection.lesion_area, 2))
        # Scale confidence (stored 0.0-1.0) to percentage for charts/templates
        try:
            confidence_scores.append(round(float(detection.confidence_score) * 100, 2))
        except Exception:
            confidence_scores.append(0.0)
    
    context = {
        'patient': patient,
        'progression_data': progression_data,
        'detection_results': detection_results,
        'treatment_plans': treatment_plans,
        'dates': dates,
        'ma_counts': ma_counts,
        'lesion_areas': lesion_areas,
        'confidence_scores': confidence_scores,
    }
    
    return render(request, 'tracking/progress.html', context)

@login_required
def progression_charts(request):
    patients = Patient.objects.filter(created_by=request.user)
    
    patient_stats = []
    for patient in patients:
        # Use detection results instead of progression data for real-time stats
        detection_results = DetectionResult.objects.filter(
            retina_image__patient=patient,
            status='completed'
        ).order_by('-detection_date')
        
        if detection_results.exists():
            latest = detection_results.first()
            previous = detection_results[1] if detection_results.count() > 1 else None
            
            if previous:
                trend = 'improving' if latest.microaneurysms_count < previous.microaneurysms_count else 'worsening' if latest.microaneurysms_count > previous.microaneurysms_count else 'stable'
            else:
                trend = 'new'
                
            patient_stats.append({
                'patient': patient,
                'latest_ma_count': latest.microaneurysms_count,
                'latest_lesion_area': latest.lesion_area,
                'detection_count': detection_results.count(),
                'trend': trend
            })
    
    return render(request, 'tracking/charts.html', {'patient_stats': patient_stats})

@login_required
def create_visit(request):
    if request.method == 'POST':
        form = PatientVisitForm(request.POST, user=request.user)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.created_by = request.user
            visit.save()
            
            recent_detection = DetectionResult.objects.filter(
                retina_image__patient=visit.patient,
                status='completed'
            ).order_by('-detection_date').first()
            
            if recent_detection:
                ProgressionData.objects.create(
                    patient=visit.patient,
                    visit=visit,
                    detection_result=recent_detection,
                    total_microaneurysms=recent_detection.microaneurysms_count,
                    total_lesion_area=recent_detection.lesion_area,
                    progression_score=calculate_progression_score(visit.patient)
                )
            
            messages.success(request, 'Patient visit recorded successfully!')
            return redirect('tracking:progression_charts')
    else:
        form = PatientVisitForm(user=request.user)
    
    return render(request, 'tracking/visit_form.html', {'form': form})

@login_required
def create_treatment_plan(request):
    if request.method == 'POST':
        form = TreatmentPlanForm(request.POST, user=request.user)
        if form.is_valid():
            treatment_plan = form.save(commit=False)
            treatment_plan.created_by = request.user
            treatment_plan.save()
            messages.success(request, 'Treatment plan created successfully!')
            return redirect('tracking:progression_charts')
    else:
        form = TreatmentPlanForm(user=request.user)
    
    return render(request, 'tracking/treatment_plan_form.html', {'form': form})

def calculate_progression_score(patient):
    progression_data = ProgressionData.objects.filter(patient=patient).order_by('visit__visit_date')
    
    if progression_data.count() < 2:
        return 0.0
    
    latest = progression_data.last()
    previous = progression_data[progression_data.count() - 2]
    
    ma_change = latest.total_microaneurysms - previous.total_microaneurysms
    area_change = latest.total_lesion_area - previous.total_lesion_area
    
    progression_score = (ma_change * 0.7 + area_change * 0.3) / 10.0
    
    return max(-10.0, min(10.0, progression_score))

@login_required
def api_progression_data(request, patient_id):
    """API endpoint for fetching chart data from detection results"""
    patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
    
    # Fetch detection results directly for real-time data
    detection_results = DetectionResult.objects.filter(
        retina_image__patient=patient,
        status='completed'
    ).select_related('retina_image').order_by('detection_date')
    
    data = {
        'dates': [d.detection_date.strftime('%b %d, %H:%M') for d in detection_results],
        'ma_counts': [d.microaneurysms_count for d in detection_results],
        'lesion_areas': [round(float(d.lesion_area), 2) for d in detection_results],
        # Scale stored 0.0-1.0 confidence to percentage (0-100) for frontend charts
        'confidence_scores': [round(float(d.confidence_score) * 100, 2) for d in detection_results],
        'total_detections': detection_results.count()
    }
    
    return JsonResponse(data)