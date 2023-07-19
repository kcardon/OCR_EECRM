from django.contrib import admin
from django.contrib.auth.models import User, Group

# Register your models here.
from persons.models import Client, Employee, Group


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "sales_contact",
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_client",
    )
    list_filter = ("sales_contact", "is_client")
    search_fields = (
        "company_name",
        "last_name",
    )
    ordering = ("company_name",)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "group_names",
        "is_staff",
    )
    list_filter = ("groups",)
    search_fields = ("last_name",)
    ordering = ("last_name",)

    def group_names(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    group_names.short_description = "Groups"


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_users",
    )

    def display_users(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    display_users.short_description = "Users"


admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
