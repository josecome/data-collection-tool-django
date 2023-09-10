from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import datetime
from django.utils.translation import gettext_lazy as _
from .models import Project_Form_Meta, Project_Form
from .forms import FieldForm, MetaForm
from .forms import CreateUserForm
from django import forms
from django.db import connections
from .utils import (
    send_activation_email, 
    send_reset_password_email, 
    send_forgotten_username_email, 
    send_activation_change_email,
)
from .decorators import admin_required, user_is_project_author
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
            clns = get_columns_of_form_and_attr(form_url)
            print(clns)
            qry = "CREATE TABLE " + form_url.replace(' ', '') + " ("
            for c in clns:
                t = tuple(c)
                cln = str(t[0]) + " " + str(t[1]) + "(" + str(t[2]) + "), "                
                qry += cln

            qry += ")" 
            qry = qry.replace(", )", ")")   
            print(qry)

            cursor = connections['default'].cursor()
            cursor.execute(qry)

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
            clns = get_columns_of_form(id)
            print(clns)
            qry = "INSERT INTO " + id.replace(' ', '') + " ("
            clns = ""
            vls = ""
            for c in clns:
                clns += c + ","
                vls = "'" + request.POST[c] + "',"

            qry += clns + ") VALUES (" + vls + ")"
            qry = qry.replace(",)", ")")
            print(qry)

            cursor = connections['default'].cursor()
            cursor.execute(qry)

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


def get_columns_of_form(id):
    clns = []
    # cs = Project_Form.objects.filter(form_meta_id=id).values('field_name')  [{'field_name': 'first_name'}, {'field_name': 'age'}]
    cs = Project_Form.objects.values_list('field_name', flat=True).filter(form_meta_id=id) # ['first_name', 'age', 'place_of_birth', 'last_name']
    for c in cs:
        clns.append(c)

    return clns


def get_columns_of_form_and_attr(id):
    cs = Project_Form.objects.values_list('field_name', 'field_type', 'field_size').filter(form_meta_id=id)
    return cs


def loginPage(request):
    if request.user.is_authenticated:
        messages.success(request, _('AAAA'))
        return redirect('/')
    else:    
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            # admin, password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                messages.success(request, _('Successfull logged in'))
                return redirect('/')           
            else:
                # Return an 'invalid login' error message.
                messages.info(request, _('Please, Invalid Username and Password!'))
            
    return render(request, 'login.html')


def registrationPage(request):
    form = CreateUserForm()
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.sucess(request, 'Account was sucessfully created for ' + user)
            
            return redirect('login.html')
                                
    context = {'form': form}
    return render(request, 'register.html', context)


@admin_required
def disable_project_by_admin():
    # Require admin
    pass


@user_is_project_author
def edit_project(request, user_id):
    # Only the author can edit the project
    pass
   
   
def logout_view(request):
    logout(request)
        
    return render(request,'logout.html')    

