"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests



#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator("06ai-P7sXy6ktpM90glcn2q8IleSHKTaZ7x1whp7TQP4")
    service = CloudantV1(authenticator = authenticator)
    service.set_service_url("https://apikey-v2-1idq9ptiz6fqglizwpenj74deckaon8rb07ljcc4y29r:65356efd3cc57ded83d59bf9c98f8dcb@448de67d-c72d-4a8f-971b-30303d11b3b7-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews',document = dict["review"]).get_result()
    try:
        result = {
            'header' : {'Content-Type':'application/json'},
            'body'   : {'data': response}
        }
        return result
    except:
        return{
            'statusCode':404,
            'message':'Something went wrong'
        }
def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
