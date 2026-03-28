from django import forms
from .models import Patient, RetinaImage
from django.core.exceptions import ValidationError
import os

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'contact_info', 'medical_history']
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter patient ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Phone, email, address...'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Diabetes duration, medications, other conditions...'}),
        }
    
    def clean_patient_id(self):
        patient_id = self.cleaned_data.get('patient_id')
        # Allow the existing patient ID when updating
        if self.instance.pk is None:  # Only validate for new records
            if Patient.objects.filter(patient_id=patient_id).exists():
                raise ValidationError('A patient with this ID already exists.')
        else:  # For updates, check if a different patient has this ID
            if Patient.objects.filter(patient_id=patient_id).exclude(pk=self.instance.pk).exists():
                raise ValidationError('A patient with this ID already exists.')
        return patient_id

class RetinaImageForm(forms.ModelForm):
    class Meta:
        model = RetinaImage
        fields = ['patient', 'original_image', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'original_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/tiff'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add any notes about this image...'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)
    
    def clean_original_image(self):
        image = self.cleaned_data.get('original_image')
        if image:
            if image.size > 10 * 1024 * 1024:
                raise ValidationError('Image file too large ( > 10MB )')
            
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
            if ext not in valid_extensions:
                raise ValidationError('Unsupported file extension. Supported: JPG, JPEG, PNG, TIFF')
        
        return image

class BatchUploadForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Use a simple CharField to bypass Django's file validation
    # We'll handle the file processing in the view
    images = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)