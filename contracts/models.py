from django.db import models
from persons.models import Client, Employee


class Contract(models.Model):
    sales_contact = models.ForeignKey(Employee, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
