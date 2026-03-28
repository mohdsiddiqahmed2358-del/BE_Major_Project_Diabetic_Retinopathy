from django import forms
from .models import PatientVisit, TreatmentPlan
from images.models import Patient

class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = PatientVisit
        fields = ['patient', 'visit_date', 'visit_number', 'visit_type', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'visit_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'visit_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'visit_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ['patient', 'plan_name', 'description', 'start_date', 'end_date', 'is_active']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")
        
        return cleaned_data