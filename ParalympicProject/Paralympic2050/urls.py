from django.urls import path, re_path
import os, sys
from Paralympic2050 import views
from .views import RegisterPage, LoginPage, AthleteDisplay, LogoutView

#### import the external pages
from .Django_external_views.homepage_view import HomePage
from .Django_external_views.Event_manage_view import EventManagement

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

    ### logout reloading
    path("logout/", LogoutView.as_view(), name="logout"),
]
