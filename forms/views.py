from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import datetime
from django.utils.translation import gettext_lazy as _
from .models import Project_Form_Meta, Project_Form
from .forms import FieldForm, MetaForm
from django.db import connections
# Create your views here.


def landingPage(request):
    messages.success(request, _('You are in Home Page, Welcome!'))
    context = {}
    context['form_deployed'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_draft'] = Project_Form_Meta.objects.filter(form_status='draft')
    context['form_arquived'] = Project_Form_Meta.objects.filter(form_status='archived')
    context['project_form'] = MetaForm()

    return render(request, 'landingpage.html', context)


def FormPage(request, id):
    messages.success(request, _('You are in Home Page, Welcome!'))
    field_form = FieldForm()
    context = {}
    context['form_id'] = Project_Form_Meta.objects.get(id=id.replace('-', ''))
    print('PP: ' + str(Project_Form_Meta.objects.get(id=id.replace('-', ''))))
    context['form_deployed'] = Project_Form_Meta.objects.filter(form_status='deployed')
    context['form_draft'] = Project_Form_Meta.objects.filter(form_status='draft')
    context['form_arquived'] = Project_Form_Meta.objects.filter(form_status='archived')
    context['form'] = field_form
    context['project_form'] = MetaForm()
    context['fields'] = Project_Form.objects.filter(form_meta_id=id.replace('-', ''))

    return render(request, 'landingpage.html', context) 


@require_http_methods(["POST"])
def CreateNewForm(request):
    if request.method == "POST":  
        form = MetaForm(request.POST)  
        if form.is_valid():  
            try:  
                form = form.save(commit=False)
                form.user_id = 1 # request.user
                form.date_created = datetime.datetime.now()
                form.date_updated = datetime.datetime.now()
                # return HttpResponse(request.POST.items())
                form.save()  
                messages.success(request, _('Successfull logged in'))
                print(str(form.id))
                return redirect('/formpage/' + str(form.id))
            except Exception as e:  
                return HttpResponse(e)
                # pass
        else:    
            messages.info(request, _('Please, fill all option of new field'))
            render(request, 'landingpage.html')

    messages.info(request, _('Something happen'))
    return redirect('/')    


@require_http_methods(["POST"])
def SubmitNewField(request):
    if request.method == "POST":  
        form = FieldForm(request.POST)
        if form.is_valid():  
            try:  
                form = form.save(commit=False)
                form_url = request.POST.get("form_url")
                form_url = form_url.replace("/formpage/", "")
                form.form_meta_id = form_url
                form.user_id = 1 # request.user
                form.created_date = datetime.datetime.now()
                form.updated_date = datetime.datetime.now()
                # return HttpResponse(request.POST.items())
                form.save()  
                messages.success(request, _('Successfull logged in'))
                return redirect('/formpage/' + form_url)  
            except Exception as e:  
                return HttpResponse(e)
                # pass
        else:    
            messages.info(request, _('Please, fill all option of new field'))
            render(request, 'landingpage.html')

    messages.info(request, _('Something happen 0'))
    return redirect('/')


def DeployForm(request):
    if request.method == "POST":  
        try:
            form_url = request.POST.get("form_url_d")
            form_url = form_url.replace("/formpage/", "")            
            f = Project_Form_Meta.objects.get(id=form_url)
            f.form_status = "deployed"
            f.updated_date = datetime.datetime.now()
            f.save()

            return redirect('/formpage/' + form_url)  
        except Exception as e:  
            return HttpResponse(e)
            # pass
    else:    
        messages.info(request, _('Error Ocurred!'))
        render(request, 'landingpage.html')

    messages.info(request, _('Error Ocurred!'))
    return redirect('/')


def ArchiveForm(request):
    if request.method == "POST":  
        try:
            form_url = request.POST.get("form_url_a")
            form_url = form_url.replace("/formpage/", "")        
            f = Project_Form_Meta.objects.get(id=form_url)
            f.form_status = "archived"
            f.updated_date = datetime.datetime.now()
            f.save()

            return redirect('/formpage/' + form_url)  
        except Exception as e:  
            return HttpResponse(e)
            # pass
    else:    
        messages.info(request, _('Error Ocurred!'))
        render(request, 'landingpage.html')

    messages.info(request, _('Error Ocurred!'))
    return redirect('/')


def DeployedFormOnline(request, id):
    if request.method == "POST":  # Insert Data In Form
        try:
            clns = ""
            vls = ""
            #request.POST['contact']
            cursor = connections['default'].cursor()
            cursor.execute("insert into clients (" + clns + ") VALUES ( " + vls + " )")
            messages.info(request, _('Form Saved Successfully!'))
        except Exception as e: 
            messages.info(request, _('Error Ocurred!'))
    else:   
        pass
    # Get Parameters and render the Form
    context = {}
    context['form'] = Project_Form_Meta.objects.get(id=id)
    context['fields'] = Project_Form.objects.filter(form_meta_id=id)

    return render(request, 'deployedform.html', context)

