from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    default_subject = "Happy birthday from {0}"
    email_subject = models.CharField(max_length=256, default=default_subject)

    default_message = "Dear [first name] [last_name],\n\nHappy birthday!\n\nSincerely,\n{0}"
    email_body = models.TextField(default=default_message)

    def __str__(self):
        return self.last_name

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    birthday = models.DateTimeField()
    email_bool = models.BooleanField('send_email', default=False)

    def __str__(self):
        return self.email
