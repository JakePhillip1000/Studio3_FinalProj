from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, re_path, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse, \
    HttpResponseRedirect, HttpResponseBadRequest
from datetime import date, datetime
from django.template import loader
from django.views import View
from django.views.generic import ListView, list
import csv
from ..models import Athletes, UserData, Event, Medal
from django.contrib import messages
import numpy as np
import json
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.db.models import Q ### I think this is for the query
from django.utils import timezone

class TicketBooking(View):
    file = "Displaying/Ticket_booking.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("date_time")
        
        #### These are the parameters for filtering
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        sport = request.GET.get("sport")
        gender = request.GET.get("gender")
        classification = request.GET.get("classification")
        location = request.GET.get("location")

        ##### This will get the date from the competition to the date to competition
        ##### (in day range), it will filter the event from the range of date that user selected
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
                events = events.filter(date_time__date__gte=date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
                events = events.filter(date_time__date__lte=date_to_obj)
            except ValueError:
                pass
    
        if sport:
            events = events.filter(sport__icontains=sport)
        if gender:
            events = events.filter(gender=gender)
        if classification:
            events = events.filter(classification__icontains=classification)
        if location:
            events = events.filter(location__icontains=location)
        
        return render(request, self.file, {"events": events})    

    def post(self, request, *args, **kwargs):
        return redirect("Paralympic2050:ticket")