from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'city']

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'schedule']