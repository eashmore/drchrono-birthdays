from django.conf.urls import url

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^account/login', views.new_session, name='new_session'),
    url(r'^loading', views.loading, name='loading'),
    url(r'', views.index, name='user_view'),
]
