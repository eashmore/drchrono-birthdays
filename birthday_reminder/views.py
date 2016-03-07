from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.http import QueryDict
from django.core import serializers

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

import requests

from .models import Doctor, Patient

def new_session_view(request):
    return render(request, 'new_session.html')

def logout_view(request):
    logout(request)
    return redirect('birthday_reminder:root_view')

def root_view(request):
    doctor = request.user.doctor
    patients = Patient.objects.filter(doctor=doctor).order_by('last_name')
    context = {
        'doctor': doctor,
        'patients': patients
    }

    return render(request, 'index.html', context)

def email_view(request):
    user = request.user
    doctor = user.doctor
    context = {
        'user': user,
        'email_subject': doctor.email_subject.format('Dr. ' + doctor.last_name),
        'email_body': doctor.email_body.format('Dr. ' + doctor.last_name)
    }

    return render(request, 'email.html', context)

# my api
class DoctorView(generic.DetailView):
    model = Doctor

    def put(self, request, **kwargs):
        doctor = User.objects.get(pk=kwargs['pk']).doctor
        updateInstance(doctor, request.body)
        doctorJSON = serializers.serialize("json", [doctor])
        return HttpResponse(doctorJSON, content_type='application/json')

class PatientView(generic.DetailView):
    model = Patient

    def put(self, request, **kwargs):
        patient = Patient.objects.get(pk=kwargs['pk'])
        updateInstance(patient, request.body)
        patientJSON = serializers.serialize("json", [patient])
        return HttpResponse(patientJSON, content_type='application/json')

def updateInstance(model, body):
    data = QueryDict(body)
    for key in data:
        value = data[key]
        if value == 'false':
            value = False

        setattr(model, key, value)

    model.save()

# parse drchrono api
def parse_drchrono_api(request):
    token_data = exchange_token(request.GET)
    header = {
        'Authorization': 'Bearer %s' % token_data['access_token'],
    }
    user = get_user(header)
    update_patients(user, header)

    user.set_password(token_data['access_token'])
    user.save()
    auth_user = authenticate(username=user.username, password=token_data['access_token'])
    login(request, auth_user)
    return redirect('birthday_reminder:root_view')

def exchange_token(params):
    if 'error' in params:
        raise ValueError('Error authorizing application: %s' % params['error'])

    content = {
        'code': params['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/loading',
        'client_id': 'g9fTx7H3gXlnZOA2SeoPmE4NV1MIh5yU4lOoxmX4',
        'client_secret': 'Kf82PCpQCpvYEkMcoWI5HH5TDaV09cVcG4IBiW7xCgZqvrm6HyEqld6P4DjU6IG3xRQn0weD1MmODkOQpLXEjiMrJ19XC9IiogwVczQWZVhWRzgEFbPf4VqqtALtNsCc',
    }
    response = requests.post('https://drchrono.com/o/token/', content)
    response.raise_for_status()
    data = response.json()
    return data

def get_user(header):
    current_doctor_data = identify_doctor(header)
    endpoint = 'doctors/{0}'.format(current_doctor_data['doctor'])
    doctor_data = get_data_from_api(endpoint, header)
    user = save_doctor(doctor_data, current_doctor_data['username'])
    return user

def identify_doctor(header):
    endpoint = 'users/current'
    current_doctor_data = get_data_from_api(endpoint, header)
    return current_doctor_data

def save_doctor(doctor_data, username):
    user = User.objects.create_user(
        id=doctor_data['id'],
        username=username,
        password='',
    )
    doctor = Doctor(
        first_name=doctor_data['first_name'],
        last_name=doctor_data['last_name'],
        user=user,
    )
    if Doctor.objects.filter(pk=user).exists():
        doctor.save(update_fields=['first_name', 'last_name'])
    else:
        doctor.save()

    return user

def get_data_from_api(endpoint, header):
    response = requests.get(
        'https://drchrono.com/api/%s' % endpoint,
        headers=header
    )
    response.raise_for_status()
    data = response.json()
    return data

def update_patients(user, header):
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        response = requests.get(patients_url, headers=header)
        data = response.json()
        for patient_data in data['results']:
            if is_valid_patient(patient_data):
                save_patient(patient_data, user)

        patients_url = data['next']

def is_valid_patient(patient_data):
    if patient_data['email'] and patient_data['date_of_birth']:
        return True

    return False

def save_patient(patient_data, user):
    patient = Patient(
        id=patient_data['id'],
        first_name=patient_data['first_name'],
        last_name=patient_data['last_name'],
        email=patient_data['email'],
        birthday=patient_data['date_of_birth'],
        doctor=user.doctor
    )
    if Patient.objects.filter(pk=patient_data['id']).exists():
        patient.save(update_fields=['first_name', 'last_name', 'email'])
    else:
        patient.save()

    return patient
