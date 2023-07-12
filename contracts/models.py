from django.db import models
from persons.models import Client, Employee


class ContractStatus(models.Model):
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.status


class Contract(models.Model):
    sales_contact = models.ForeignKey(Employee, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(ContractStatus, on_delete=models.PROTECT)
    amount = models.FloatField()
    payment_due = models.DateTimeField()
