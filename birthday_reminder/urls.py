from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^accounts/login/$', views.new_session_view, name='new_session'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^loading/$', views.parse_api, name='loading'),
    url(
        r'^$', login_required(views.PatientIndexView.as_view()),
        name='patient_index'
    ),
    url(r'^email/$', login_required(views.email_view), name="custom_email"),

    url(
        r'^api/doctor/(?P<doctor_id>[0-9]+)/$',
        login_required(views.api_doctor), name='doctor'
    ),
    url(
        r'^api/patients/$',
        login_required(views.api_patients_index), name='patients'
       ),
    url(
        r'^api/patient/(?P<patient_id>[0-9]+)/$',
        login_required(views.api_patient), name='patient'
    ),
]
