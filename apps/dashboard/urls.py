from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^add_appointment$', views.add_appointment, name="add_appointment"),
    url(r'^update_appointment/(?P<id>\d+)$', views.update_appointment, name="update_appointment"),
    url(r'^appointments/(?P<id>\d+)$', views.edit_app, name="edit_app"),
    url(r'^delete_app/(?P<id>\d+)$', views.delete_app, name="delete_app"),
    # url(r'^dashboard$', views.dashboard),


]
