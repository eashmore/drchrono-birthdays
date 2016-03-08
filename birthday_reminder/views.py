from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.http import QueryDict
from django.core import serializers

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

import requests

from .models import Doctor, Patient

# Login view
def new_session_view(request):
    return render(request, 'sessions/new_session.html')

# Redirect from drchrono. Handles user login and updating db with new drchrono data
def auth_view(request):
    if 'error' in request.GET:
        return redirect('birthday_reminder:session_error')

    user = parse_drchrono_api(request.GET)
    auth_user = authenticate(
        username=user.username,
        password=user.doctor.set_random_user_password()
    )
    login(request, auth_user)
    return redirect('birthday_reminder:index_view')

# If drchrono auth fails
def session_error_view(request):
    return render(request, 'sessions/session_error.html')

def logout_view(request):
    logout(request)
    return redirect('birthday_reminder:index_view')

# Landing page after login
def index_view(request):
    doctor = request.user.doctor
    patients = Patient.objects.filter(doctor=doctor).order_by('last_name')
    context = {
        'doctor': doctor,
        'patients': patients
    }

    return render(request, 'index.html', context)

def edit_email_view(request):
    user = request.user
    doctor = user.doctor
    context = {
        'user': user,
        'email_subject': doctor.email_subject.format(doctor.last_name),
        'email_body': doctor.email_body.format(doctor.last_name)
    }

    return render(request, 'doctors/email.html', context)

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

# Updates instance model with new data
def updateInstance(model, request_body):
    data = QueryDict(request_body)
    for key in data:
        value = data[key]
        if value == 'false':
            value = False

        setattr(model, key, value)

    model.save()

# Get data from drchrono api
def parse_drchrono_api(request_params):
    access_token = exchange_token(request_params)
    current_doctor_data = get_doctor_data(access_token)
    user = save_user(current_doctor_data)
    update_patients(user, access_token)
    return user

# Get access token
def exchange_token(params):
    content = {
        'code': params['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/auth/',
        'client_id': 'g9fTx7H3gXlnZOA2SeoPmE4NV1MIh5yU4lOoxmX4',
        'client_secret': 'Kf82PCpQCpvYEkMcoWI5HH5TDaV09cVcG4IBiW7xCgZqvrm6HyEqld6P4DjU6IG3xRQn0weD1MmODkOQpLXEjiMrJ19XC9IiogwVczQWZVhWRzgEFbPf4VqqtALtNsCc',
    }
    response = requests.post('https://drchrono.com/o/token/', content)
    response.raise_for_status()
    data = response.json()
    return data['access_token']

# Find doctor data for current drchrono user
def get_doctor_data(access_token):
    header = {'Authorization': 'Bearer %s' % access_token}
    user_data = get_current_user_data(header)

    doctor_endpoint = 'doctors/{0}'.format(user_data['doctor'])
    data = get_data_from_drchrono(doctor_endpoint, header)
    data['username'] = user_data['username']
    return data

# Find user data for current drchrono user
def get_current_user_data(header):
    endpoint = 'users/current'
    current_doctor_data = get_data_from_drchrono(endpoint, header)
    return current_doctor_data

def save_user(doctor_data):
    user = User.objects.create_user(
        id=doctor_data['id'],
        username=doctor_data['username'],
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

# Find the current user's patients and insert/update patient's row in db
def update_patients(user, access_token):
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        response = requests.get(patients_url, headers={
            'Authorization': 'Bearer %s' % access_token
        })
        data = response.json()
        for patient_data in data['results']:
            if is_valid_patient(patient_data):
                save_patient(patient_data, user)

        patients_url = data['next']

# Patient is only valid if they have both an email and a birthday
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
        patient.save(
            update_fields=['first_name', 'last_name', 'email', 'birthday']
        )
    else:
        patient.save()

    return patient

def get_data_from_drchrono(endpoint, header):
    response = requests.get(
        'https://drchrono.com/api/%s' % endpoint,
        headers=header
    )
    response.raise_for_status()
    data = response.json()
    return data
