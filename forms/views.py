from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Project_Form_Meta
# Create your views here.


def landingPage(request):
    messages.success(request, _('You are in Home Page, Welcome!'))
    context = {}
    context['form_deployed'] = Project_Form_Meta.objects.all()
    context['form_draft'] = Project_Form_Meta.objects.all()
    context['form_arquived'] = Project_Form_Meta.objects.all()
    return render(request, 'landingpage.html', context) 