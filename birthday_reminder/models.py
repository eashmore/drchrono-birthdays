from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import string
import random

EMAIL_SUBJECT = "Happy birthday from Dr. {0}"
EMAIL_MESSAGE = "Dear [first name] [last name],\n\nHappy birthday!\n\nSincerely,\nDr. {0}"

class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email_subject = models.CharField(
        max_length=256, default=EMAIL_SUBJECT
    )
    email_body = models.TextField(default=EMAIL_MESSAGE)

    def __str__(self):
        return self.last_name

    def set_random_password(self):
        user = self.user
        all_chars = string.letters + string.digits + string.punctuation
        password = ''.join((random.choice(all_chars)) for x in range(20))
        user.set_password(password)
        user.save()
        return password

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    birthday = models.DateTimeField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.email
