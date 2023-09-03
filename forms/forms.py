from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms  
from .models import Project_Form, Project_Form_Meta


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class FieldForm(forms.ModelForm):  
    class Meta:  
        model = Project_Form
        fields = ["field_name", "field_label", "field_description", "field_type", "field_size"]


class MetaForm(forms.ModelForm):  
    class Meta:  
        model = Project_Form_Meta
        fields = ["form_name","form_description","form_country","form_field"]