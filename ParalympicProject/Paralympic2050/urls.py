from django.urls import path, re_path
from Paralympic2050 import views

app_name = "Paralympic2050"

urlpatterns = [
    path('', views.TestPage, name='tester')
]
