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
from django.db.models import Q ### I think this is for the query
from django.utils import timezone

class TicketBooking(View):
    file = "Displaying/Ticket_booking.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("date_time")

        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        sport = request.GET.get("sport")
        gender = request.GET.get("gender")
        classification = request.GET.get("classification")
        location = request.GET.get("location")

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

        ####### The available button will filter out only the available event
        available_only = request.GET.get("available")
        if available_only == "1":
            events = events.filter(status="In Progress")

        return render(request, self.file, {"events": events})

    def post(self, request, *args, **kwargs):
        print("POST data received:", dict(request.POST)) 
        
        username = request.session.get("logged_in_user")
        if not username:
            return redirect("Paralympic2050:ticket")

        try:
            user = UserData.objects.get(username=username)
        except UserData.DoesNotExist:
            return redirect("Paralympic2050:ticket")

        event_id = request.POST.get("event_id")
        
        if not event_id:
            return redirect("Paralympic2050:ticket")
        
        try:
            event_id = int(event_id)
        except (ValueError, TypeError):
            return redirect("Paralympic2050:ticket")

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return redirect("Paralympic2050:ticket")

        ticket_fields = [
            ["ticket_standard_A", "standard", "A", "price_standard_A"],
            ["ticket_disability_A", "disability", "A", "price_disability_A"],
            ["ticket_companion_A", "companion", "A", "price_companion_A"],
            ["ticket_under14_A", "under14", "A", "price_under14_A"],
            ["ticket_under14_disability_A", "under14_disability", "A", "price_under14_disability_A"],
            ["ticket_standard_B", "standard", "B", "price_standard_B"],
            ["ticket_disability_B", "disability", "B", "price_disability_B"],
            ["ticket_companion_B", "companion", "B", "price_companion_B"],
            ["ticket_under14_B", "under14", "B", "price_under14_B"],
            ["ticket_under14_disability_B", "under14_disability", "B", "price_under14_disability_B"],
        ]

        created_tickets = []
        total_tickets = 0

        for field_name, ticket_type, category, price_field in ticket_fields:
            quantity_str = request.POST.get(field_name, "0")
            price_str = request.POST.get(price_field, "0")

            try:
                quantity = int(quantity_str)
                price = float(price_str)
            except ValueError:
                continue

            if quantity > 0:
                ticket = Ticket.objects.create(
                    user=user,
                    event=event,
                    category=category,
                    ticket_type=ticket_type,
                    quantity=quantity,
                    total_price=quantity * price,
                )

                created_tickets.append(ticket)
                total_tickets += quantity
                print(f"Created ticket: {ticket_type} {category} x{quantity}")  # Debug print

        if not created_tickets:
            messages.error(request, "No tickets were selected.")
            return redirect("Paralympic2050:ticket")

        return redirect("Paralympic2050:ticket")
    
    