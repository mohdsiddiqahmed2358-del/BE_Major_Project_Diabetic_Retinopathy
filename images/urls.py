from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('upload/', views.image_upload, name='upload'),
    path('batch-upload/', views.batch_upload, name='batch_upload'),
    path('images/', views.image_list, name='image_list'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),
    path('images/<int:pk>/delete/', views.delete_image, name='delete_image'),
]