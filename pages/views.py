from django.views.generic import TemplateView
from django.shortcuts import render
from accounts.models import Preapproval

class HomePageView(TemplateView):
    template_name = 'home.html'