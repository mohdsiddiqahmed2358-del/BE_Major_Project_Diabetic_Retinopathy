import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import PatientForm, RetinaImageForm, BatchUploadForm
from .models import Patient, RetinaImage

@login_required
def patient_list(request):
    patients = Patient.objects.filter(created_by=request.user).annotate(
        image_count=Count('retina_images')
    ).order_by('-created_at')
    return render(request, 'images/patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, f'Patient {patient.patient_id} created successfully!')
            return redirect('images:patient_list')
    else:
        form = PatientForm()
    return render(request, 'images/patient_form.html', {'form': form, 'title': 'Create Patient'})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.patient_id} updated successfully!')
            return redirect('images:patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'images/patient_form.html', {'form': form, 'title': 'Update Patient'})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    images = patient.retina_images.all().select_related('detection_result')
    return render(request, 'images/patient_detail.html', {
        'patient': patient,
        'images': images
    })

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = RetinaImageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            
            file_extension = os.path.splitext(image.original_image.name)[1].upper().replace('.', '')
            if file_extension in ['JPG', 'JPEG']:
                image.image_format = 'JPEG'
            elif file_extension == 'PNG':
                image.image_format = 'PNG'
            elif file_extension == 'TIFF':
                image.image_format = 'TIFF'
            
            image.save()
            messages.success(request, 'Image uploaded successfully! Now you can run detection on it.')
            return redirect('images:image_detail', pk=image.pk)
    else:
        form = RetinaImageForm(user=request.user)
    
    return render(request, 'images/image_upload.html', {'form': form})

@login_required
def batch_upload(request):
    if request.method == 'POST':
        form = BatchUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            images = request.FILES.getlist('images')  # Get all files
            
            if not images:
                messages.error(request, 'Please select at least one image to upload.')
                return render(request, 'images/batch_upload.html', {'form': form})
            
            successful_uploads = 0
            uploaded_image_ids = []
            
            for image_file in images:
                try:
                    # Validate file size
                    if image_file.size > 10 * 1024 * 1024:
                        messages.warning(request, f'Skipped {image_file.name}: File too large (max 10MB)')
                        continue
                    
                    # Validate file extension
                    file_extension = os.path.splitext(image_file.name)[1].lower()
                    valid_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
                    if file_extension not in valid_extensions:
                        messages.warning(request, f'Skipped {image_file.name}: Unsupported file format')
                        continue
                    
                    retina_image = RetinaImage(
                        patient=patient,
                        original_image=image_file,
                        uploaded_by=request.user
                    )
                    
                    # Set image format
                    ext = file_extension.upper().replace('.', '')
                    if ext in ['JPG', 'JPEG']:
                        retina_image.image_format = 'JPEG'
                    elif ext == 'PNG':
                        retina_image.image_format = 'PNG'
                    elif ext == 'TIFF':
                        retina_image.image_format = 'TIFF'
                    
                    retina_image.save()
                    successful_uploads += 1
                    uploaded_image_ids.append(retina_image.pk)
                    
                except Exception as e:
                    messages.warning(request, f'Failed to upload {image_file.name}: {str(e)}')
            
            if successful_uploads > 0:
                messages.success(request, f'Successfully uploaded {successful_uploads} out of {len(images)} images. You can now run detection on them.')
                # If only one image, redirect to detail page for immediate detection
                if successful_uploads == 1:
                    return redirect('images:image_detail', pk=uploaded_image_ids[0])
            else:
                messages.error(request, 'No images were successfully uploaded.')
            
            return redirect('images:image_list')
    else:
        form = BatchUploadForm(user=request.user)
    
    return render(request, 'images/batch_upload.html', {'form': form})

@login_required
def image_list(request):
    images = RetinaImage.objects.filter(uploaded_by=request.user).select_related('patient', 'detection_result')
    return render(request, 'images/image_list.html', {'images': images})

@login_required
def image_detail(request, pk):
    image = get_object_or_404(RetinaImage, pk=pk, uploaded_by=request.user)
    detection_result = getattr(image, 'detection_result', None)
    
    return render(request, 'images/image_detail.html', {
        'image': image,
        'detection_result': detection_result
    })

@login_required
def delete_image(request, pk):
    image = get_object_or_404(RetinaImage, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        image_name = image.original_image.name
        image.delete()
        messages.success(request, f'Image {image_name} deleted successfully.')
        return redirect('images:image_list')
    
    return render(request, 'images/delete_confirm.html', {'object': image, 'type': 'image'})