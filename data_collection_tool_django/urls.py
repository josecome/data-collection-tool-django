"""data_collection_tool_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from forms import views as form_views

urlpatterns = [
    path('', form_views.landingPage, name='landingpage'),
    path('formpage/<str:id>', form_views.FormPage, name='formpage'),
    path('deployed/<str:id>', form_views.DeployedFormOnline, name='formpage'),
    path('createnewform/', form_views.CreateNewForm, name='createnewform'),
    path('newfield/submitnewfield/', form_views.SubmitNewField, name='submitnewfield'),
    path('deployform/', form_views.DeployForm, name='deployform'),
    path('archiveform/', form_views.ArchiveForm, name='deployform'),
    path('admin/', admin.site.urls),
]
