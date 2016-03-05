from django.conf.urls import url

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
