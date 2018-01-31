
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages import error
from .models import Appointment
from ..login.models import User
from django.db.models import Q

from datetime import datetime, date
from time import strftime



def index(request):
    return render(request, 'dashboard/dashboard.html')

def success(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.error, 'please login.')
        return redirect('/')
    context = {
    	# 'appointments': Appointment.objects.filter(Q(date__gte=datetime.now()) & Q(user__id=request.session['user_id'])).exclude(date__lte=datetime.now(), date__gte=datetime.now()).order_by('date'),
		'todays_apps':Appointment.objects.exclude(date=datetime.now(), user_id=request.session['user_id']).order_by('time'),
		# 'todays_date':Appointment.objects.filter(date=datetime.now(), user_id=request.session['user_id'])
        'other_apps':Appointment.objects.filter(date=datetime.now(), user_id=request.session['user_id']).order_by('time'),
		}

    return render(request, "dashboard/dashboard.html", context)


def edit_app(request, id):
	context = {
		'appointments':Appointment.objects.get(id=id)
		}
	return render(request, 'dashboard/edit_appt.html', context)

def update_appointment(request, id):
	if request.method == 'POST':
		update_appointment = Appointment.appointmentManager.edit_appointment(id, request.POST)
		if update_appointment[0] == False:
			for error in update_appointment[1]:
				messages.add_message(request, messages.INFO, error)
			return redirect(reverse('edit_app', kwargs={'id':id}))
		else:
			return redirect('/success')
	else:
		pass


def add_appointment(request):
    print request.POST
    new_appointment = Appointment.appointmentManager.add_appointment(request.POST)
    if new_appointment[0] == False:
        for error in new_appointment[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/success')
    else:
        Appointment.objects.create(date=request.POST['date'], time=request.POST['time'], name=request.POST['name'], status="pending", user=User.objects.get(id=request.session['user_id']))
	return redirect('/success')

def delete_app(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('/success')
