from django.urls import path, re_path
import os, sys
from Paralympic2050 import views
from .views import RegisterPage, LoginPage, AthleteDisplay, LogoutView, VideoIntroPage

#### import the external pages
from .Django_external_views.homepage_view import HomePage
from .Django_external_views.Event_manage_view import EventManagement
from .Django_external_views.Medal_summary_view import MedalSummary
from .Django_external_views.Ticket_booking import TicketBooking
from .Django_external_views.shop import Shopping

#### Application name
app_name = "Paralympic2050"

urlpatterns = [
    ### Homepage
    path("", HomePage.as_view(), name="home"),

    #### Other pages
    path("register/", RegisterPage.as_view(), name="register"),
    path("login/", LoginPage.as_view(), name="login"),
    path("athletes/", AthleteDisplay.as_view(), name="athletes"),
    path("event/", EventManagement.as_view(), name = "event"),
    path("medals/", MedalSummary.as_view(), name = "medals"),
    path("ticket/", TicketBooking.as_view(), name = "ticket"),
    path("shop/", Shopping.as_view(), name = "shop"),
    path("video_intro/", VideoIntroPage.as_view(), name="kirito_intro"),


    ### logout reloading
    path("logout/", LogoutView.as_view(), name="logout"),
]
