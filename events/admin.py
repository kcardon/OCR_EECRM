from django.contrib import admin

# Register your models here.
from events.models import Event, EventStatus


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "support_contact",
        "event_status",
        "event_date",
    )
    list_filter = ("event_status", "support_contact")
    search_fields = ("client", "support_contact")

    ordering = ("event_date",)


admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus)
