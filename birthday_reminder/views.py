from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import requests

from .models import Patient

def new_session(request):
    return render(request, 'new_session.html')

@login_required(login_url='account/login')
def index(request):
    return render(request, 'user_view.html')

def loading(request):
    token_data = exchange_token(request.GET)
    header = {
        'Authorization': 'Bearer %s' % token_data['access_token'],
    }
    doctor = get_doctor(header)
    user = authenticate(username=doctor.username, password='')
    login(request, user)
    get_valid_patients(doctor, header)
    return redirect('birthday_reminder:user_view')

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


def get_doctor(header):
    current_doctor_data = identify_doctor(header)
    endpoint = 'doctors/%s' % current_doctor_data['doctor']
    doctor_data = get_data_from_api(endpoint, header)
    doctor = save_doctor(doctor_data, current_doctor_data['username'])
    return doctor

def identify_doctor(header):
    endpoint = 'users/current'
    current_doctor_data = get_data_from_api(endpoint, header)
    return current_doctor_data

def get_data_from_api(endpoint, header):
    response = requests.get('https://drchrono.com/api/%s' % endpoint,
                            headers=header
                            )
    response.raise_for_status()
    data = response.json()
    return data

def save_doctor(doctor_data, username):
    doctor = User.objects.create_user(id=doctor_data['id'],
                    first_name=doctor_data['first_name'],
                    last_name=doctor_data['last_name'],
                    username=username,
                    password='',
                   )
    doctor.save()
    return doctor

def get_valid_patients(doctor, header):
    endpoint = 'patients?search=doctor:%s' % doctor.id
    patients = get_data_from_api(endpoint, header)
    for patient_data in patients['results']:
        if is_valid_patient(patient_data):
            save_patients(patient_data, doctor)

def save_patients(patient_data, doctor):
    patient = Patient(id=patient_data['id'],
                      first_name=patient_data['first_name'],
                      last_name=patient_data['last_name'],
                      email=patient_data['email'],
                      birthday=patient_data['date_of_birth'],
                      doctor=doctor
                     )
    patient.save()

def is_valid_patient(patient_data):
    if patient_data['email'] and patient_data['date_of_birth']:
        return True

    return False
