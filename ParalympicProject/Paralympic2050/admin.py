from django.contrib import admin
from .models import Athletes, UserData

'''
username: admin
password: admin1234
'''

# This is for athletes model management
### This will make it show inside the admin page (in form format)
@admin.register(Athletes)
class AthletesAdmin(admin.ModelAdmin):
    list_display = ("bid", "firstName", "lastName", "country", "gender")
    search_fields = ("bid", "firstName", "lastName", "country", "email", "gender")

### This is the register form (can fill inside the admin page)
@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    display = ("username", "password")
