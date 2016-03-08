from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^accounts/login/$', views.new_session_view, name='new_session'),
    url(r'^accounts/error/$', views.session_error_view, name='session_error'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^$', login_required(views.index_view), name='index_view'),
    url(r'^email/$', login_required(views.edit_email_view), name="custom_email"),

    url(r'^api/doctor/(?P<pk>[0-9]+)/$',
        login_required(views.DoctorView.as_view()), name='doctor'
       ),
    url(r'^api/patient/(?P<pk>[0-9]+)/$',
        login_required(views.PatientView.as_view()), name='patient'
       ),
]
