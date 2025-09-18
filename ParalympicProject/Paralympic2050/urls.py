from django.urls import path, re_path
from Paralympic2050 import views
from .views import RegisterPage, LoginPage, AthleteDisplay

app_name = "Paralympic2050"

urlpatterns = [
    path("register/", RegisterPage.as_view(), name="register"),
    path("login/", LoginPage.as_view(), name="login"),
    path("athletes/", AthleteDisplay.as_view(), name="athletes"),
]
