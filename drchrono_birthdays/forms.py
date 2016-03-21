from django import forms

from models import Doctor, Patient


class EmailForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['email_subject', 'email_body']


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['send_email']
