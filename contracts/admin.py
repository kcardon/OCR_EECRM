from django.contrib import admin

# Register your models here.
from contracts.models import Contract, ContractStatus

class ContractStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(Contract)
