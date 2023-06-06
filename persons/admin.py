from django.contrib import admin

# Register your models here.
from persons.models import Client, Employee

admin.site.register(Client)
admin.site.register(Employee)