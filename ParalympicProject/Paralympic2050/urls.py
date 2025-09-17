from django.urls import path, re_path
from Paralympic2050 import views
from .views import RegisterPage

app_name = "Paralympic2050"

urlpatterns = [
    path("", RegisterPage.as_view(), name="register")
]
