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

class MedalSummary(View):
    file_name = "Displaying/Medal_summary.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        medals = Medal.objects.all()

        if query:
            medals = medals.filter(team__icontains=query)
        return render(request, self.file_name, {"medals": medals, "query": query})

    def post(self, request, *args, **kwargs):
        event_id = request.POST.get("event-id")
        if event_id:
            Medal.objects.filter(id=event_id).delete()
            return redirect('Paralympic2050:medals')

        team_id = request.POST.get("team-id")
        team_name = request.POST.get("team-name")
        gold = int(request.POST.get("gold", 0))
        silver = int(request.POST.get("silver", 0))
        bronze = int(request.POST.get("bronze", 0))
        total = gold + silver + bronze

        if team_name:
            if team_id:
                medal = Medal.objects.get(id=team_id)
                medal.team = team_name
                medal.gold = gold
                medal.silver = silver
                medal.bronze = bronze
                medal.total = total
                medal.save()
            else:
                Medal.objects.create(
                    team = team_name,
                    gold = gold,
                    silver = silver,
                    total = total,
                )
        
        return redirect("Paralympic2050:medals")
