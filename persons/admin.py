from django.contrib import admin
from django.contrib.auth.models import User, Group

# Register your models here.
from persons.models import Client, Employee, Group

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone',) 

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name',)  

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_users',)
    def display_users(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])
    display_users.short_description = 'Users'

admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
