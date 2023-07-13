from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser


class Person(models.Model):
    class Meta:
        abstract = True

    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class CustomUser(Person, AbstractUser):
    pass


class Employee(CustomUser):
    def __str__(self):
        return self.first_name + " " + self.last_name

    pass


class Client(Person):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    sales_contact = models.ForeignKey(Employee, on_delete=models.PROTECT)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
