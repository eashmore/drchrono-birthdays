from django.shortcuts import render
import requests

from .models import Doctor, Patient

def new_session(request):
    return render(request, 'new_session.html')

def index(request):
    token_data = exchange_token(request.GET)
    user_data = get_user_data(token_data['access_token'])
    save_user(user_data)
    return render(request, 'index.html')

def exchange_token(params):
    if 'error' in params:
        raise ValueError('Error authorizing application: %s' % params['error'])

    content = {
        'code': params['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/reminders',
        'client_id': 'g9fTx7H3gXlnZOA2SeoPmE4NV1MIh5yU4lOoxmX4',
        'client_secret': 'Kf82PCpQCpvYEkMcoWI5HH5TDaV09cVcG4IBiW7xCgZqvrm6HyEqld6P4DjU6IG3xRQn0weD1MmODkOQpLXEjiMrJ19XC9IiogwVczQWZVhWRzgEFbPf4VqqtALtNsCc',
    }
    response = requests.post('https://drchrono.com/o/token/', content)
    response.raise_for_status()
    data = response.json()
    return data


def get_user_data(access_token):
    header = {
        'Authorization': 'Bearer %s' % access_token,
    }
    user_id = identify_user(header)
    endpoint = 'doctors/%s' % user_id
    user_data = get_data_from_api(endpoint, header)
    return user_data

def identify_user(header):
    endpoint = 'users/current'
    current_user_data = get_data_from_api(endpoint, header)
    return current_user_data['doctor']

def get_data_from_api(endpoint, header):
    response = requests.get('https://drchrono.com/api/%s' % endpoint,
                            headers=header
                            )
    response.raise_for_status()
    data = response.json()
    return data

def save_user(user_data):
    user = Doctor(id=user_data['id'],
                  first_name=user_data['first_name'],
                  last_name=user_data['last_name']
                 )
    user.save()
