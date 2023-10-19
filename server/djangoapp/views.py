from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def get_static(request):
    context = {}
    if request.method == "GET":
        return render(request, 'static.html', context)


def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



def get_contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context={}

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['psw']
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)



def logout_request(request):
    
    print("Log out the user `{}`".format(request.user.username))
   
    logout(request)
    context = {}
    return  render(request, 'djangoapp/index.html', context)



def registration(request):
    context = {}
   
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
      
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return  render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
'''def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
'''
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealerId):
     if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/review-get"
        # Get dealers from the URL
        dealer_details = get_dealer_reviews_from_cf(url,dealerId)
        # Concat all dealer's short name
        dealer_reviews = ' '.join([detail.review for detail in dealer_details])
        # Return a list of dealer short name
        return HttpResponse(dealer_reviews)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

