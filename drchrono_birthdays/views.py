from django.core import serializers
from django.views import generic
from django.http import HttpResponse
from django.utils.http import urlquote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from drchrono_project.settings import CLIENT_DATA
from models import Doctor, Patient
from utils import get_drchrono_user, update_instance

def login_view(request):
    return render(request, 'sessions/login.html', context={
        'redirect_url': urlquote(CLIENT_DATA['redirect_url']),
        'client_id': CLIENT_DATA['client_id']
    })

def oauth_view(request):
    """
    Redirect destination for drchrono. Handles user login and updating db with
    new drchrono data.
    """
    if 'error' in request.GET:
        return redirect('drchrono_birthdays:login_error')

    user = get_drchrono_user(request.GET)
    auth_user = authenticate(
        username=user.username,
        password=user.doctor.set_random_password()
    )
    login(request, auth_user)
    return redirect('drchrono_birthdays:index_view')

def login_error_view(request):
    """
    If drchrono authentication fails
    """
    return render(request, 'sessions/error.html')

def logout_view(request):
    logout(request)
    return redirect('drchrono_birthdays:index_view')

def index_view(request):
    """
    Landing page after login
    """
    doctor = request.user.doctor
    patients = doctor.patient_set.order_by('last_name')
    context = {
        'doctor': doctor,
        'patients': patients,
        'username': request.user.username,
        'redirect_url': urlquote(CLIENT_DATA['redirect_url']),
        'client_id': CLIENT_DATA['client_id']
    }

    return render(request, 'index.html', context)

def edit_email_view(request):
    user = request.user
    doctor = user.doctor
    context = {
        'user': user,
        'email_subject': doctor.email_subject.format(doctor.last_name),
        'email_body': doctor.email_body.format(doctor.last_name),
    }

    return render(request, 'doctors/email.html', context)

def patient_search_view(request):
    if request.method == 'POST':
        patients = request.user.doctor.patient_set
        query_string = request.POST['queryString']
        patients = patients.filter(
            Q(last_name__contains=query_string) |
            Q(first_name__contains=query_string) |
            Q(email__contains=query_string)
        )

    return render(request, 'patients/patient_list.html', {'patients': patients})

# My API
class DoctorView(generic.DetailView):
    model = Doctor

    def put(self, request, **kwargs):
        doctor = get_object_or_404(User, pk=kwargs['pk']).doctor
        update_instance(doctor, request.body)
        doctorJSON = serializers.serialize("json", [doctor])
        return HttpResponse(doctorJSON, content_type='application/json')

class PatientView(generic.DetailView):
    model = Patient

    def put(self, request, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        update_instance(patient, request.body)
        patientJSON = serializers.serialize("json", [patient])
        return HttpResponse(patientJSON, content_type='application/json')
