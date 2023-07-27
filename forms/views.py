from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# Create your views here.


def landingPage(request):
    messages.success(request, _('You are in Home Page, Welcome!'))
    return render(request, 'landingpage.html') 