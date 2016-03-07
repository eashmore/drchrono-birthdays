from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^accounts/login/$', views.new_session_view, name='new_session'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^loading/$', views.parse_drchrono_api, name='loading'),
    url(r'^$', login_required(views.RootView.as_view()),name='root_view'),
    url(r'^email/$', login_required(views.email_view), name="custom_email"),

    url(r'^api/doctor/(?P<pk>[0-9]+)/$',
        login_required(views.DoctorView.as_view()), name='doctor'
       ),
    url(r'^api/patient/(?P<pk>[0-9]+)/$',
        login_required(views.PatientView.as_view()), name='patient'
       ),
]
