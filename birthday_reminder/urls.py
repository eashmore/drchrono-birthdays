from django.conf.urls import url

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^account/login', views.new_session, name='new_session'),
    url(r'^loading', views.parse_api, name='loading'),
    url(r'', views.user_view, name='user_view'),
]
