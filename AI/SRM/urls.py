from . import views
from django.urls import path


urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('batch/', views.batch_list, name='batch_list'),
    path('batch/create/', views.batch_create, name='batch_create'),
    path('get-recordings/', views.get_recording, name='get-recordings'),

 
]
