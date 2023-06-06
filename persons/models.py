from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Person(models.Model):
    class Meta:
        abstract = True
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    

class Employee(Person, User):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

class Client(Person):
    company_name = models.CharField(max_length=250)
    sales_contact = models.ForeignKey(Employee, on_delete=models.PROTECT)

