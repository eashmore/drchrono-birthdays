from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^accounts/login/$', views.new_session, name='new_session'),
    url(r'^loading', views.parse_api, name='loading'),
    url(r'^$', login_required(views.PatientIndexView.as_view()), name='patient_index'),

    url(r'^api/patients', views.api_patients_index, name='patients'),
    url(r'^api/patient/(?P<pk>[0-9]+)', views.api_patient, name='patient'),
]
