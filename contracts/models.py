from django.db import models
from persons.models import Client, Employee

from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def __str__(self):
        return self.client.company_name


@receiver(post_save, sender=Contract)
def update_client_status(sender, instance, **kwargs):
    """Met à jour la valeur "is_client" de l'objet client pour la passer en "True" dès lors qu'un contrat est signé."""
    client = Client.objects.get(pk=instance.client.id)
    if instance.status != "Draft" and client.is_client == False:
        client.is_client = True
        client.save()
