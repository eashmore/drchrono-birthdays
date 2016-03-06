from django.conf.urls import url

from . import views

app_name = 'birthday_reminder'
urlpatterns = [
    url(r'^$', views.new_session, name='new_session'),
    url(r'^loading', views.loading, name='loading'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user_view'),
]
