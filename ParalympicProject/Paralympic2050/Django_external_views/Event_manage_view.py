from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect, HttpResponseBadRequest
from datetime import date, datetime
from django.template import loader
from django.views import View
from django.views.generic import ListView, list
import csv
from ..models import Athletes, UserData, Event
from django.contrib import messages
import numpy as np
import json
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.db.models import Q ### I think this is for the query
from django.utils import timezone

class EventManagement(View):
    file_name = "Displaying/Event_management.html"
    
    def get(self, request, *args, **kwargs):
        #### THis part is the search query. I will filtered it out by
        ##### the query sport and number
        search_query = request.GET.get("q")
        events = Event.objects.all().order_by("date_time")
        
        if search_query:
            events = events.filter(
                Q(number__icontains=search_query) | Q(sport__icontains=search_query)
            )
        
        ev_query = {
            "events": events,
            "query": search_query,
        }

        events = Event.objects.all().order_by("date_time")
        return render(request, self.file_name, ev_query)

    def post(self, request, *args, **kwargs):
        ### Check whether the user is admin or not
        if request.session.get("logged_in_user") != "admin":
            messages.error(request, "You have no permission")
            return redirect("Paralympic2050:event")
        
        event_id = request.POST.get("event-id") 

        date = request.POST.get("event-date")
        number = request.POST.get("event-number")
        time = request.POST.get("event-time")
        sport = request.POST.get("event-sport")
        gender = request.POST.get("gender")
        classification = request.POST.get("event-classification")
        phrase = request.POST.get("event-phrase")
        status = request.POST.get("event-status")
        location = request.POST.get("location")

        if request.POST.get("event-id") and not (date and time and sport):
            try:
                event = Event.objects.get(id=event_id)
                event.delete()
                messages.success(request, "Event deleted successfully.")
            except Event.DoesNotExist:
                messages.error(request, "Event not found for deletion.")
            return redirect("Paralympic2050:event")
        
        if date and time and sport and gender and classification:
            date_time_str = f"{date} {time}"
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

            if event_id:
                try:
                    event = Event.objects.get(id=event_id)
                    event.date_time = date_time
                    event.number = number
                    event.sport = sport
                    event.gender = gender
                    event.classification = classification
                    event.phrase = phrase
                    event.status = status
                    event.location = location
                    event.save()
                    messages.success(request, "Event updated successfully.")
                except Event.DoesNotExist:
                    messages.error(request, "Event dont found")
            else:
                ###### This method, we will create the objects for the event data
                #### This wil be used on the backend side (can manage using postgreSQL)
                Event.objects.create(
                    date_time=date_time,
                    number=number,
                    sport=sport,
                    gender=gender,
                    classification=classification,
                    phrase=phrase,
                    status=status,
                    location=location,
                )
                messages.success(request, "Event added successfully.")
        else:
            messages.error(request, "Please fill all required event fields.")

        return redirect("Paralympic2050:event")

