from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from images.models import Patient
from detection.models import DetectionResult
from tracking.models import ProgressionData
from .models import Report

@login_required
def generate_report(request):
    patients = Patient.objects.filter(created_by=request.user)
    
    # Get query parameters for pre-selection
    selected_patient_id = request.GET.get('patient')
    report_type = request.GET.get('type', 'detection')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        report_type = request.POST.get('report_type')
        report_format = request.POST.get('format')
        
        patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
        
        if report_format == 'PDF':
            if report_type == 'detection':
                return generate_detection_pdf(request, patient)
            elif report_type == 'progression':
                return generate_progression_pdf(request, patient)
            elif report_type == 'comprehensive':
                return generate_comprehensive_pdf(request, patient)
        else:
            # Excel generation would go here
            messages.info(request, 'Excel report generation coming soon!')
            return redirect('reports:generate')
    
    context = {
        'patients': patients,
        'selected_patient_id': selected_patient_id,
        'report_type': report_type,
    }
    
    return render(request, 'reports/generate.html', context)

def generate_detection_pdf(request, patient):
    """Generate PDF report for detection results"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Center aligned
    )
    title = Paragraph(f"Microaneurysm Detection Report - {patient.first_name} {patient.last_name}", title_style)
    story.append(title)
    
    # Patient Information
    story.append(Paragraph("Patient Information", styles['Heading2']))
    patient_info = [
        ["Patient ID:", patient.patient_id],
        ["Name:", f"{patient.first_name} {patient.last_name}"],
        ["Date of Birth:", patient.date_of_birth.strftime("%Y-%m-%d")],
        ["Gender:", patient.get_gender_display()],
    ]
    patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Detection Results
    detection_results = DetectionResult.objects.filter(
        retina_image__patient=patient,
        retina_image__uploaded_by=request.user
    ).select_related('retina_image')
    
    story.append(Paragraph("Detection Results Summary", styles['Heading2']))
    
    if detection_results:
        summary_data = [
            ["Total Images Processed", len(detection_results)],
            ["Total Microaneurysms Detected", sum(result.microaneurysms_count for result in detection_results)],
            ["Average Confidence Score", f"{sum(result.confidence_score for result in detection_results) / len(detection_results):.2f}"],
        ]
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed Results
        story.append(Paragraph("Detailed Detection Results", styles['Heading3']))
        detailed_data = [["Image", "Date", "Microaneurysms", "Lesion Area", "Confidence"]]
        
        for result in detection_results:
            detailed_data.append([
                result.retina_image.original_image.name.split('/')[-1],
                result.detection_date.strftime("%Y-%m-%d"),
                str(result.microaneurysms_count),
                f"{result.lesion_area:.2f} px²",
                f"{result.confidence_score:.2f}"
            ])
        
        detailed_table = Table(detailed_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        detailed_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        story.append(detailed_table)
    else:
        story.append(Paragraph("No detection results available for this patient.", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Paragraph("Generated by RetinaDetect System", styles['Italic']))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF value from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="detection_report_{patient.patient_id}.pdf"'
    response.write(pdf)
    
    # Save report record
    Report.objects.create(
        patient=patient,
        report_type='detection',
        report_format='PDF',
        generated_by=request.user,
        report_file=f"detection_report_{patient.patient_id}.pdf",
        parameters={'format': 'PDF'}
    )
    
    return response

def generate_progression_pdf(request, patient):
    """Generate PDF report for patient progression"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,
    )
    title = Paragraph(f"Patient Progression Report - {patient.first_name} {patient.last_name}", title_style)
    story.append(title)
    
    # Patient Information
    story.append(Paragraph("Patient Information", styles['Heading2']))
    patient_info = [
        ["Patient ID:", patient.patient_id],
        ["Name:", f"{patient.first_name} {patient.last_name}"],
        ["Date of Birth:", patient.date_of_birth.strftime("%Y-%m-%d")],
    ]
    patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Progression Data
    progression_data = ProgressionData.objects.filter(
        patient=patient
    ).select_related('visit', 'detection_result').order_by('visit__visit_date')
    
    story.append(Paragraph("Progression Overview", styles['Heading2']))
    
    if progression_data:
        progression_info = [
            ["Total Visits", len(progression_data)],
            ["First Visit", progression_data.first().visit.visit_date.strftime("%Y-%m-%d")],
            ["Latest Visit", progression_data.last().visit.visit_date.strftime("%Y-%m-%d")],
        ]
        
        if len(progression_data) > 1:
            first = progression_data.first()
            latest = progression_data.last()
            ma_change = latest.total_microaneurysms - first.total_microaneurysms
            area_change = latest.total_lesion_area - first.total_lesion_area
            
            progression_info.extend([
                ["Microaneurysm Change", f"{ma_change:+.0f}"],
                ["Lesion Area Change", f"{area_change:+.2f} px²"],
            ])
        
        progression_table = Table(progression_info, colWidths=[2.5*inch, 2.5*inch])
        progression_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(progression_table)
        story.append(Spacer(1, 20))
        
        # Visit Details
        story.append(Paragraph("Visit Details", styles['Heading3']))
        visit_data = [["Visit", "Date", "Microaneurysms", "Lesion Area", "Progression Score"]]
        
        for data in progression_data:
            visit_data.append([
                f"Visit {data.visit.visit_number}",
                data.visit.visit_date.strftime("%Y-%m-%d"),
                str(data.total_microaneurysms),
                f"{data.total_lesion_area:.2f} px²",
                f"{data.progression_score:+.2f}"
            ])
        
        visit_table = Table(visit_data, colWidths=[1*inch, 1*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        visit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        story.append(visit_table)
    else:
        story.append(Paragraph("No progression data available for this patient.", styles['Normal']))
    
    # Clinical Notes
    if progression_data:
        story.append(Spacer(1, 20))
        story.append(Paragraph("Clinical Assessment", styles['Heading3']))
        
        latest = progression_data.last()
        if len(progression_data) > 1:
            previous = progression_data[len(progression_data)-2]
            ma_trend = "improving" if latest.total_microaneurysms < previous.total_microaneurysms else "worsening" if latest.total_microaneurysms > previous.total_microaneurysms else "stable"
            assessment = f"The patient shows {ma_trend} microaneurysm count compared to the previous visit."
        else:
            assessment = "Baseline assessment completed. Monitor progression in subsequent visits."
        
        story.append(Paragraph(assessment, styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Paragraph("Generated by RetinaDetect System", styles['Italic']))
    
    # Build PDF
    doc.build(story)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="progression_report_{patient.patient_id}.pdf"'
    response.write(pdf)
    
    # Save report record
    Report.objects.create(
        patient=patient,
        report_type='progression',
        report_format='PDF',
        generated_by=request.user,
        report_file=f"progression_report_{patient.patient_id}.pdf",
        parameters={'format': 'PDF'}
    )
    
    return response

def generate_comprehensive_pdf(request, patient):
    """Generate comprehensive PDF report"""
    # For now, just generate detection report as comprehensive
    # You can enhance this to combine both detection and progression data
    return generate_detection_pdf(request, patient)