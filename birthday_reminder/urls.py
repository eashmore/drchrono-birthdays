from django.conf.urls import url

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^$', views.new_session, name='new_session'),
    url(r'^reminders', views.index, name='index'),
]
