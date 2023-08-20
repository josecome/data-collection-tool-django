from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import datetime
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


@require_http_methods(["POST"])
def SubmitNewField(request):
    if request.method == "POST":  
        form = FieldForm(request.POST)  
        if form.is_valid():  
            try:  
                form = form.save(commit=False)
                form.user_id = 1 # request.user
                form.date_created = datetime.datetime.now()
                form.date_updated = datetime.datetime.now()
                # return HttpResponse(request.POST.items())
                form.save()  
                messages.success(request, _('Successfull logged in'))
                return redirect('/contents/create_content')  
            except Exception as e:  
                return HttpResponse(e)
                # pass
        else:    
            messages.info(request, _('Please, fill all option of new field'))
            return render(request, '/')  

    messages.info(request, _('Something happen'))
    return redirect('/')    

