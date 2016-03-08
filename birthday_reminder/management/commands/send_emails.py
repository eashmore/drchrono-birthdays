from django.core.management.base import BaseCommand
from birthday_reminder.models import Doctor
from django.core.mail import send_mail


import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def email_bday_patients(doctor):
            patient_set = doctor.patient_set
            for patient in patient_set.all():
                if is_birthday(patient):
                    email_patient(doctor, patient)


        def is_birthday(patient):
            currentDate = datetime.date.today()
            birthday = patient.birthday
            if birthday.month == currentDate.month and birthday.day == currentDate.day:
                return True

            return False

        def email_patient(doctor, patient):
            subject = doctor.email_subject.replace('[first name]', patient.first_name).replace('[last name]', patient.last_name)
            body = doctor.email_body.replace('[first name]', patient.first_name).replace('[last name]', patient.last_name)
            send_mail(subject, body, 'drchrono.birthday.reminder@gmail.com', [patient.email], fail_silently=False)

        doctors = Doctor.objects.all()
        for doctor in doctors:
            email_bday_patients(doctor)
