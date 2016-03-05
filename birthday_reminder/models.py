from __future__ import unicode_literals

from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    birthday = models.DateTimeField()
