from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect, HttpResponseBadRequest
from datetime import date, datetime
from django.template import loader
from django.views import View
from django.views.generic import ListView, list
import csv
from .models import Athletes, UserData
from django.contrib import messages
import numpy as np
import json
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.db.models import Q ### I think this is for the query

############## Register page
class RegisterPage(View): #### This is like GET and POST method in HTML forms handling
    def get(self, request):
        return render(request, "Registering/register.html")

    def post(self, request):
        username =  request.POST.get("username").strip()
        password = request.POST.get("password")
        conpass = request.POST.get("conpass")

        ### Already exist username
        if UserData.objects.filter(username=username).exists():
            data = {
                "username_taken": True,
                "taken_username": username
            }
            return render(request, "Registering/register.html", data)

        if (password is None) or (password != conpass):
            cont = {
                "password_mismatch": True,
                "err": "Password not match",
            }
            return render(request, "Registering/register.html", cont)
      
        ###### When the username is same
        if UserData.objects.filter(username__iexact=username).exists():
            return render(request, "Registering/register.html", {
                "username_taken": True,
                "taken_username": username
            })
        
        ##### Saving thje username to the db
        UserData.objects.create(username = username, password = password)
        
        return redirect("Paralympic2050:login")

############ The login page
class LoginPage(View):
    def get(self, request):
        return render(request, "Registering/login.html")
    
    def post(self, request):
        username = request.POST.get("username").strip()
        password = request.POST.get("password")

        if not UserData.objects.filter(username=username).exists():
            datas = {
                "username_not_exist": True, 
                "entered_username": username,
                "not_exist": True,           
                "enter_user": username
            }
            return render(request, "Registering/login.html", datas)

        try:
            user = UserData.objects.get(username__iexact=username)
        except UserData.DoesNotExist:
            return render(request, "Registering/login.html", {
                "not_exist": True,
                "enter_user": username,
            })

        if user.password != password:
            return render(request, "Registering/login.html", {
                "wrong_password": True,
                "entered_username": username,
            })
        
        #### stored inside the session variable (it can be called in any page)
        request.session['logged_in_user'] = user.username
        
        return redirect("Paralympic2050:athletes")

########### Athlete display page
class AthleteDisplay(ListView):
    temp = "Displaying/Athletes_display.html"
    
    def get(self, request, *args, **kwargs):
        ###### This is for the search features
        key = request.GET.get("keyword", "").strip()
        gender = request.GET.get("gender", "").strip()

        athletes = Athletes.objects.all()

        if key is not None:
           athletes = athletes.filter(
               Q(firstName__icontains=key) | Q(lastName__icontains=key)
           )

        if gender is not None:
            athletes = athletes.filter(gender__iexact=gender)

        ath_dictionary = {"athletes": athletes, "keyword": key, "gender": gender}
        return render(request, self.temp, ath_dictionary)
    
    def post(self, request, *args, **kwargs):
        athlete_id = request.POST.get("athlete_id")
        if athlete_id is not None:
            try:
                athlete = get_object_or_404(Athletes, id=athlete_id)
                athlete.delete()
            except Athletes.DoesNotExist:
                messages.error(request, "Athletes not found")
        athletes = Athletes.objects.all()
        ath_data = {"athletes": athletes}
        return render(request, self.temp, ath_data)

##### Logged out view
class LogoutView(View):
    def post(self, request):
        print("Before logout: {}".format( request.session.get('logged_in_user')))
        
        logout(request) 
        request.session.pop("logged_in_user", None)

        if "logged_in_user" in request.session:
            del request.session['logged_in_user']
        
        print("After logout: {}".format(request.session.get('logged_in_user')))
            
        return JsonResponse({"status": "logged out"})