from django.shortcuts import render
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from datetime import date, datetime
from django.template import loader
from django.views import View
import csv
from django.contrib import messages
import numpy as np
import json

class RegisterPage(View):
    def get(self, request):
        return render(request, "register.html")