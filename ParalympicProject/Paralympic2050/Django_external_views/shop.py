from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect, HttpResponseBadRequest
from datetime import date, datetime
from django.template import loader
from django.views import View
from django.views.generic import ListView, list
import csv
from ..models import Athletes, UserData, Event, Medal, Ticket
from django.contrib import messages
import numpy as np
import json
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

class Shopping(View):
    file = "Displaying/shop.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.file)

    def post(self, request, *args, **kwargs):
        return redirect("Paralympic2050:shop")

class AboutPage(View):
    about_file = "Displaying/about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.about_file)

    def post(self, request, *args, **kwargs):
        return redirect("Paralympic2050:about")
    
    