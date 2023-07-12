from django.contrib import admin

# Register your models here.
from contracts.models import Contract, ContractStatus


class ContractStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status")


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "status",
        "date_created",
        "amount",
    )
    list_filter = (
        "status",
        "client",
    )
    search_fields = ("client",)
    ordering = ("client",)


admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(Contract, ContractAdmin)
