from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import User
from django.contrib import messages
from django.contrib.messages import error
from django.contrib import *
# Create your views here.

# ('/')

def index(request):
    return render(request, 'login/index.html')

# ('/register')
def register(request):
    results = User.objects.validate(request.POST)
    if results['status'] == True:
        user = User.objects.creator(request.POST)
        messages.error(request, 'User has been created')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/')

# ('/login')
def login(request):
    results = User.objects.loginVal(request.POST)
    if results['status'] == False:
        messages.error(request, 'Please check your Email and Password and try again')
        return redirect('/')
    request.session['email'] = results['user'].email
    request.session['first_name'] = results['user'].first_name
    request.session['user_id'] = results['user'].id

    return redirect('/success')
# ('/logout')
def logout(request):
    request.session.clear()
    return redirect('/')
