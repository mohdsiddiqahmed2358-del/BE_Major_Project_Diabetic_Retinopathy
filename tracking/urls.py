from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('progress/<int:patient_id>/', views.patient_progress, name='patient_progress'),
    path('charts/', views.progression_charts, name='progression_charts'),
    path('visit/create/', views.create_visit, name='create_visit'),
    path('treatment-plan/create/', views.create_treatment_plan, name='create_treatment_plan'),
    path('api/progression/<int:patient_id>/', views.api_progression_data, name='api_progression_data'),
]