from django import forms  
from .models import Project_Form, Project_Form_Meta


class FieldForm(forms.ModelForm):  
    class Meta:  
        model = Project_Form
        fields = ["field_name", "field_label", "field_description", "field_type", "field_size"]


class MetaForm(forms.ModelForm):  
    class Meta:  
        model = Project_Form_Meta
        fields = ["form_name","form_description","form_country","form_field"]