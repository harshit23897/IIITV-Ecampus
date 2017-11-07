from django import forms
from .models import CourseMaterial, AssignmentMaterial

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('description', 'file', )

class AssignmentMaterialForm(forms.ModelForm):
    class Meta:
        model = AssignmentMaterial
        fields = ('description', 'file', )