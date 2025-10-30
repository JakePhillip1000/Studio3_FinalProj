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
import sys, os

######## (This is how to get the latest version of code in github)
####### git fetch origin
######## git reset --hard origin/main

###### importing the external pages
from .Django_external_views.homepage_view import HomePage

############## Register page
class RegisterPage(View): #### This is like GET and POST method in HTML forms handling
    def get(self, request):
        return render(request, "Registering/register.html")

    def post(self, request):
        username =  request.POST.get("username").strip()
        password = request.POST.get("password")
        conpass = request.POST.get("conpass")

        ##### I have created the admin account
        #### This method will prevetnt from registering into admin account
        if username.lower() == "admin":
            return render(request, "Registering/register.html", {
                "username_taken": True,
                "taken_username": username,
                "reserved_name": True,
                "err": "DO NOT USE THE ADMIN ACCOUNT"  
            })

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
            #### Failed to login, return to the same page
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

        #### Admin account and permission
        if username.lower() == "admin":
            request.session["is_admin"] = True
        else:
            request.session["is_admin"] = False

        ### Detect whether the user name is kirito, if kirito 
        #### something good will happen (The video kirito will show)
        if username.lower() == "kirito":
            request.session["show_video"] = True
            return redirect("Paralympic2050:kirito_intro")
        
        return redirect("Paralympic2050:home") ### After login, go to the home page

#### This will show if user login as kirito
### this is the video views 'Link Start'
class VideoIntroPage(View):
    def get(self, request):
        if not request.session.get("show_video", False):
            return redirect("Paralympic2050:home")
        
        del request.session["show_video"]
        return render(request, "Registering/kirito_intro.html")
    

########### Athlete display page
class AthleteDisplay(ListView):
    temp = "Displaying/Athletes_display.html"
    
    def get(self, request, *args, **kwargs):
        ###### This is for the search features
        key = request.GET.get("keyword", "").strip()
        gender = request.GET.get("gender", "").strip()

        athletes = Athletes.objects.all()

        if key:
           athletes = athletes.filter(
               Q(firstName__icontains=key) | Q(lastName__icontains=key)
           )
        
        if gender and gender.lower() != "all":
            athletes = athletes.filter(gender__iexact = gender)

        if gender:
            athletes = athletes.filter(gender__iexact=gender)

        ath_dictionary = {"athletes": athletes, "keyword": key, "gender": gender}
        return render(request, self.temp, ath_dictionary)
    
class AthleteDisplay(ListView):
    temp = "Displaying/Athletes_display.html"

    def get(self, request, *args, **kwargs): #### This will works for search and filter in django
        key = request.GET.get("keyword", "").strip()
        gender = request.GET.get("gender", "").strip()

        athletes = Athletes.objects.all().order_by("firstName", "lastName")  # Alphabetical sorting

        if key:
           athletes = athletes.filter(
               Q(firstName__icontains=key) | Q(lastName__icontains=key)
           )
        
        if gender and gender.lower() != "all":
            athletes = athletes.filter(gender__iexact=gender)

        ath_dictionary = {"athletes": athletes, "keyword": key, "gender": gender}
        return render(request, self.temp, ath_dictionary)
    
        
    def post(self, request, *args, **kwargs):
        #### Check whether the user is admin or not
        if request.session.get("logged_in_user") != "admin":
            messages.error("No permission to edit, delete and add")
            return redirect("Paralympic2050:athletes")

        #### Delete selected athletes 
        delete_ids = request.POST.getlist("delete_ids")

        if delete_ids:
            Athletes.objects.filter(id__in=delete_ids).delete()
            messages.success(request, f"Deleted {len(delete_ids)} athlete(s).")
            athletes = Athletes.objects.all().order_by('firstName', 'lastName')
            return render(request, self.temp, {"athletes": athletes})

        ####### Edit the athlete information
        athlete_id = request.POST.get("athlete_id")
        
        if athlete_id:
            athlete = get_object_or_404(Athletes, id=athlete_id)
            athlete.firstName = request.POST.get("firstName", athlete.firstName)
            athlete.lastName = request.POST.get("lastName", athlete.lastName)
            athlete.gender = request.POST.get("gender", athlete.gender)
            
            if request.POST.get("age"):
                athlete.age = request.POST.get("age")
            athlete.save()
            messages.success(request, "Successfully updated")

        ####### Add new athlete into the database
        bib = request.POST.get("bib")
        classification = request.POST.get("classification")
        country = request.POST.get("country")
        first_name = request.POST.get("first_name")
        surname = request.POST.get("surname")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        dob = request.POST.get("date_of_birth")

        if (bib and classification and country and first_name and surname):
            new_athlete = Athletes.objects.create(
                bid=bib,
                classification=classification,
                country=country,
                firstName=first_name,
                lastName=surname,
                gender=gender,
                email= email if email else None,
                dateOfBirth = dob,
            )
            messages.success(request, f"Athlete {first_name} {surname} added")

        ##### Now this will filter athletes orderby alphabetical order
        athletes = Athletes.objects.all().order_by("firstName", "lastName")
        return redirect("Paralympic2050:athletes")

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

###### Homepage, this page is actually inside another folder.
### This is just an class instance (the real homepage is in Django_exteral_veiws)
class Home2(View):
    def get(self, request, *args, **kwargs):
        homepage = HomePage()
        return homepage.get(request)

###### This is the end of the code of the views.py
#### For further, I've created a external view in Django_external_views folder

