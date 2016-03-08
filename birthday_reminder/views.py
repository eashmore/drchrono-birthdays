from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.http import QueryDict
from django.core import serializers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from .models import Doctor, Patient
from utils import get_drchrono_user

# Login view
def login_view(request):
    return render(request, 'sessions/login.html')

# Redirect from drchrono. Handles user login and updating db with new drchrono data
def oauth_view(request):
    if 'error' in request.GET:
        return redirect('birthday_reminder:login_error')

    user = get_drchrono_user(request.GET)
    auth_user = authenticate(
        username=user.username,
        password=user.doctor.set_random_password()
    )
    login(request, auth_user)
    return redirect('birthday_reminder:index_view')

# If drchrono auth fails
def login_error_view(request):
    return render(request, 'sessions/error.html')

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
        update_instance(doctor, request.body)
        doctorJSON = serializers.serialize("json", [doctor])
        return HttpResponse(doctorJSON, content_type='application/json')

class PatientView(generic.DetailView):
    model = Patient

    def put(self, request, **kwargs):
        patient = Patient.objects.get(pk=kwargs['pk'])
        update_instance(patient, request.body)
        patientJSON = serializers.serialize("json", [patient])
        return HttpResponse(patientJSON, content_type='application/json')

# Updates instance model with new data
def update_instance(model, request_body):
    data = QueryDict(request_body)
    for key in data:
        value = data[key]
        if value == 'false':
            value = False

        setattr(model, key, value)

    model.save()
