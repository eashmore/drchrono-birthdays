from django.core.management.base import BaseCommand
from birthday_reminder.models import Doctor
from django.core.mail import send_mass_mail

import datetime
import kronos

@kronos.register('0 0 * * *')
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def get_bday_emails(doctor):
            emails = []
            patient_set = doctor.patient_set
            for patient in patient_set.all():
                if is_birthday(patient):
                    message = (generate_email(doctor, patient))
                    emails.append(message)

            return emails

        def is_birthday(patient):
            currentDate = datetime.date.today()
            birthday = patient.birthday
            if birthday.month == currentDate.month and birthday.day == currentDate.day:
                return True

            return False

        def generate_email(doctor, patient):
            subject = doctor.email_subject.format(doctor.last_name)
            subject = subject.replace('[first name]', patient.first_name)
            subject = subject.replace('[last name]', patient.last_name)

            body = doctor.email_body.format(doctor.last_name)
            body = body.replace('[first name]', patient.first_name)
            body = body.replace('[last name]', patient.last_name)

            message = (subject, body, 'edashmore@gmail.com',
                       [patient.email]
                      )
            return message

        doctors = Doctor.objects.all()
        for doctor in doctors:
            emails = get_bday_emails(doctor)
            send_mass_mail(tuple(emails), fail_silently=False)
