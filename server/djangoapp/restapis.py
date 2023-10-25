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


def get_dealers_from_cf(url):
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
def get_dealer_by_id_from_cf(url, id):
    
    dealers = get_dealers_from_cf(url)
    dealer = [x for x in dealers if x.id == id]
    print (dealer)
    return dealer[0]


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
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                   car_model=review["car_model"], car_year=review["car_year"],
                                   sentiment=analyze_review_sentiments(review["review"]),id=review["_id"])
            if len(json.loads(review_obj.sentiment)["keywords"]) > 0 :
                senti =json.loads(review_obj.sentiment)["keywords"][0]["sentiment"]['label']
            else:
                senti = 'neutral'
            review_obj.sentiment=senti
            results.append(review_obj)

    return results

'''
def post_request(url, json_payload):
        
    try:
        api_key = "ApiKey-b8714c0c-7627-4e3b-b4a5-0ae93eXXXXXX"
        headers = {
           'Content-Type': 'application/json'           
        }
        response = requests.post(url, headers=headers, params=json_payload)
        status_code = response.status_code
        json_resp = json.load(response.text)
        print(response.text)
        return json_resp
    except:
         return{'message':'Something went wrong'}
'''
    
def post_request(url, json_payload, **kwargs):
    #url =  "https://ritikaj-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
   
    
    response = requests.post(url, params=kwargs, json=json_payload)
    print (response.text)
    return response
     