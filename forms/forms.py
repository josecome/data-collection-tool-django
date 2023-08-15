from django import forms  
from .models import Project_Form


class FieldForm(forms.ModelForm):  
    class Meta:  
        model = Project_Form
        fields = ["field_name", "field_description", "field_type", "field_size"]