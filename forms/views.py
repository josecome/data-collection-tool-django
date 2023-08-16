from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Project_Form_Meta
from .forms import FieldForm
# Create your views here.


def landingPage(request):
    messages.success(request, _('You are in Home Page, Welcome!'))
    context = {}
    context['form_deployed'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_draft'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_arquived'] = Project_Form_Meta.objects.filter(form_status='deployed')

    return render(request, 'landingpage.html', context)


def FormPage(request, id):
    messages.success(request, _('You are in Home Page, Welcome!'))
    field_form = FieldForm()
    context = {}
    context['form_id'] = Project_Form_Meta.objects.get(pk=id.replace('-', ''))
    context['form_deployed'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_draft'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_arquived'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form'] = field_form

    return render(request, 'landingpage.html', context) 

