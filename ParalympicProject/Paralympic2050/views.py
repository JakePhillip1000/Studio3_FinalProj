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

def TestPage(request):
    page = loader.get_template("testpage.html")
    return HttpResponse(page.render())