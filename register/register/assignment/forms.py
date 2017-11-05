from django import forms
from .models import CourseMaterial

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('description', 'file', 'course_no', )