from django.shortcuts import render
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from datetime import date, datetime
from django.template import loader
from django.views import View
from django.views.generic import ListView, list
import csv
from .models import Athletes
from django.contrib import messages
import numpy as np
import json

class RegisterPage(View):
    def get(self, request):
        return render(request, "Registering/register.html")
    
class LoginPage(View):
    def get(self, request):
        return render(request, "Registering/login.html")

class AthleteDisplay(ListView):
    temp = "Displaying/Athletes_display.html"
    
    def get(self, request, *args, **kwargs):
        athletes = Athletes.objects.all()
        ath_dictionary  = {"athletes": athletes}
        return render(request, self.temp, ath_dictionary)