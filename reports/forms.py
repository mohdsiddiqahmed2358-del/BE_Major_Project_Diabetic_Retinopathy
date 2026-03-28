from django import forms
from images.models import Patient
from django.utils import timezone

class ReportGenerationForm(forms.Form):
    REPORT_TYPES = (
        ('detection', 'Detection Report'),
        ('progression', 'Progression Report'),
        ('comprehensive', 'Comprehensive Report'),
        ('patient_summary', 'Patient Summary'),
    )
    
    FORMAT_CHOICES = (
        ('PDF', 'PDF Document'),
        ('EXCEL', 'Excel Spreadsheet'),
    )
    
    report_type = forms.ChoiceField(
        choices=REPORT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        initial='PDF',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    date_to = forms.DateField(
        required=False,
        initial=timezone.now().date,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    include_images = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    include_charts = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_to < date_from:
            raise forms.ValidationError("End date cannot be before start date.")
        
        return cleaned_data