from django.contrib import admin
from .models import Athletes

'''
username: admin
password: admin1234
'''

# This is for athletes model management
@admin.register(Athletes)
class AthletesAdmin(admin.ModelAdmin):
    list_display = ("bid", "firstName", "lastName", "country", "gender")
    search_fields = ("bid", "firstName", "lastName", "country", "email", "gender")
