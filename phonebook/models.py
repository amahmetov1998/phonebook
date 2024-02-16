from django.db import models


class Phonebook(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    surname = models.CharField(max_length=100, db_index=True)
    middle_name = models.CharField(max_length=100)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    employee_phone_number = models.CharField(max_length=20, unique=True)
    mobile_phone_number = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ('surname',)


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
