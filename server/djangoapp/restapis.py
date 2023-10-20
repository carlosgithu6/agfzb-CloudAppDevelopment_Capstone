#import requests
#import json
# import related models here
#from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions,EntitiesOptions, KeywordsOptions
ulr_NLU = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/629f860d-192a-41c5-b953-57d1d60c4f6b"
api_key_NLU = "QOhKCsOu5jYSuiXEWe6rrH2MBweeHHM_TuVkjhGxg3yh"
def get_request_watson(url, data):
    print(data)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
       api_key = "QOhKCsOu5jYSuiXEWe6rrH2MBweeHHM_TuVkjhGxg3yh"
       response = requests.get(url, params=data,
                                headers={'Content-Type': 'application/json','Authorization':f'Bearer {api_key}'},
                              )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters

        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def analyze_review_sentiments(dealerreview):
    authenticator = IAMAuthenticator(api_key_NLU)
   
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator )
    natural_language_understanding.set_service_url(ulr_NLU)
    response = natural_language_understanding.analyze(
    text=dealerreview,
    features=Features(entities=EntitiesOptions(emotion=True, sentiment=True, limit=2), keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()
    return json.dumps(response, indent=2)


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
          
            # Create a CarDealer object with values in `doc` object
            reviews_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                   car_model=review["car_model"], car_year=review["car_year"],
                                   sentiment=analyze_review_sentiments(review["review"]),id=review["_id"])
            
            results.append(reviews_obj)

    return results



    
   
    