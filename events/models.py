from django.db import models
from persons.models import Client, Employee
from contracts.models import Contract

class EventStatus(models.Model):
    status = models.CharField(max_length=25)


class Event(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(Employee, on_delete=models.PROTECT)
    event_status = models.ForeignKey(EventStatus, on_delete=models.PROTECT)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
