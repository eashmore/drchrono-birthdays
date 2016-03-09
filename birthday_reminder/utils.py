from django.http import QueryDict
from django.contrib.auth.models import User
import requests

from models import Doctor, Patient

def update_instance(model, request_body):
    """
    Updates instance model with new data
    """
    data = QueryDict(request_body)
    for key in data:
        value = data[key]
        if value == 'false':
            value = False

        setattr(model, key, value)

    model.save()

# Access drchrono api
def get_drchrono_user(request_params):
    """
    Get user data from drchrono api and update user and patients rows in db
    """
    access_token = exchange_token(request_params)
    current_doctor_data = get_doctor_data(access_token)
    user = save_user(current_doctor_data)
    update_patients(user, access_token)
    return user

def exchange_token(params):
    """
    Get access token from drchrono
    """
    content = {
        'code': params['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://drchrono-bday-reminder.herokuapp.com/oauth/',
        'client_id': 'g9fTx7H3gXlnZOA2SeoPmE4NV1MIh5yU4lOoxmX4',
        'client_secret': 'Kf82PCpQCpvYEkMcoWI5HH5TDaV09cVcG4IBiW7xCgZqvrm6HyEqld6P4DjU6IG3xRQn0weD1MmODkOQpLXEjiMrJ19XC9IiogwVczQWZVhWRzgEFbPf4VqqtALtNsCc',
    }
    response = requests.post('https://drchrono.com/o/token/', content)
    response.raise_for_status()
    data = response.json()
    return data['access_token']

def get_doctor_data(access_token):
    """
    Get doctor data for current drchrono user
    """
    header = {'Authorization': 'Bearer %s' % access_token}
    user_data = get_user_data(header)

    doctor_endpoint = 'doctors/{0}'.format(user_data['doctor'])
    data = get_drchrono_data(doctor_endpoint, header)
    data['username'] = user_data['username']
    return data

def get_user_data(header):
    """
    Get user data for current drchrono user
    """
    endpoint = 'users/current'
    current_doctor_data = get_drchrono_data(endpoint, header)
    return current_doctor_data

def save_user(doctor_data):
    user = User.objects.create_user(
        id=doctor_data['id'],
        username=doctor_data['username'],
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

def update_patients(user, access_token):
    """
    Find the current user's patients and insert/update patient's row in db
    """
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

def is_valid_patient(patient_data):
    """
    Checks is a patient is valid.
    Patients are only valid if they have both an email and a birthday.
    """
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

def get_drchrono_data(endpoint, header):
    """
    Helper function to get data the from the drchrono api
    """
    response = requests.get(
        'https://drchrono.com/api/%s' % endpoint,
        headers=header
    )
    response.raise_for_status()
    data = response.json()
    return data
