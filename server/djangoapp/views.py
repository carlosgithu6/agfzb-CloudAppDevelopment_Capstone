from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf,post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from .models import CarModel
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
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
        context = {}
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)
    

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealerId):
     if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/review-get"
        urldealers = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/dealerships"

        # Get dealers from the URL
        dealer_details = get_dealer_reviews_from_cf(url,dealerId)
        context = {}
        context["reviewslist"]=dealer_details
        context["dealer_name"]=get_dealer_by_id_from_cf(urldealers,dealerId).full_name
        context["dealerId"]=dealerId
        # Concat all dealer's short name
        #dealer_reviews = ' '.join([str(detail.sentiment) for detail in dealer_details])
        # Return a list of dealer short name
        #return HttpResponse(dealer_reviews)
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
'''
@csrf_exempt

def add_review(request, dealer_id):
   url_post= "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/review-post"
   #if request.user.is_authenticated:
   if request.method =='POST':
        review={
                "time": datetime.utcnow().isoformat(),
                "name": request.data["name"],
                "dealership": dealer_id,
                "review": request.data["review"],
                "purchase": request.data["purchase"],
                "purchase_date": request.data["purchase_date"],
                "car_make": request.data["car_make"],
                "car_model": request.data["car_model"],
                "car_year": request.data["car_year"]
        }
        json_payload = {"review":review}
        json_resp = post_request(url_post, json_payload)
        return HttpResponse(json_resp)
'''

def add_review(request, dealer_id):
    context = {}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/dealerships"
    dealer = get_dealer_by_id_from_cf(url, id=dealer_id)
   
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        context["dealer_id"]=dealer_id
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.Make
           # payload["car_model"] = car.name
            payload["car_year"] = int(car.Year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/fc04fac8-e44c-4b0a-b76c-2e0fe1d23c5b/dealership-package/review-post"
            review = {
                "id":id,
                "time":datetime.utcnow().isoformat(),
                "name":request.user.username,  # Assuming you want to use the authenticated user's name
                "dealership" :id,                
                "review": request.POST["content"],  # Extract the review from the POST request
                "purchase": True,  # Extract purchase info from POST
                "purchase_date":request.POST["purchasedate"],  # Extract purchase date from POST
                "car_make": car.Make,  # Extract car make from POST
                #"car_model": car.name,  # Extract car model from POST
                "car_year": int(car.Year.strftime("%Y")),  # Extract car year from POST
            }
            review=json.dumps(review,default=str)
            new_payload1 = {}
            new_payload1["review"] = review
            print("\nREVIEW:",review)
            post_request(review_post_url, review, id = dealer_id)
        return redirect("djangoapp:dealer_details", dealerId = dealer_id)

