from __future__ import unicode_literals

from django.db import models
from ..login.models import User
from datetime import datetime, date
from time import strftime
# Create your models here.

class AppointmentManager(models.Manager):
    def add_appointment(self, post_data):
        errors = []
        results = {}
        if post_data['date'] == "" or post_data['date'] == strftime('%Y-%m-%d'):
            errors.append("Date can not be blank. Please add the current date or a future date.")
        if post_data['time'] == "":
            errors.append("Please add a Time to this Appointment.")
        if not len(post_data['name']) > 1:
            errors.append("Please give your Appointment a Unique Name.")
        if post_data['date'] != "" and  Appointment.objects.filter(date=post_data['date']) and Appointment.objects.filter(time=post_data['time']):
            errors.append("Already have an Appointment at this time.")
        if not errors:
            # new_appointment=Appointment.objects.create(name=appointment[0], date=appointment[1], time=appointment[2])
            return (True, post_data)

        return (False, errors)

    def edit_appointment(self, id, post_data):
        appointment = Appointment.objects.get(id=id)
        errors = []

        if post_data['date'] == "" or post_data['date'] < strftime('%Y-%m-%d'):
            errors.append("Date can not be blank. Please add the current date or a future date.")

        if post_data['time'] == "":
            errors.append("Please add a Time to this Appointment.")

        if not len(post_data['name']) > 1:
            errors.append("Please give your Appointment a Unique Name.")
        if errors:
            return (False, errors)
        else:
            appointment.name = post_data['name']
            appointment.date = post_data['date']
            appointment.time = post_data['time']
            appointment.status = post_data['status']
            appointment.save()

            return (True, appointment)


class Appointment(models.Model):
	date = models.DateField()
	time = models.TimeField()
	name = models.CharField(max_length=50)
	status = models.CharField(max_length=50)
	user = models.ForeignKey(User, related_name="usersappts")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	appointmentManager = AppointmentManager()
	objects = models.Manager()
