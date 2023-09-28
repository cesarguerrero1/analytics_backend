'''
Cesar Guerrero
08/24/23

The Twitter Dashboard Service is how we interact with the Twitter API for Dashboard services.
We will be curating all the data here before returning it to the controller.

'''

import os
import requests
from flask import (json, session, Response, jsonify)
from requests_oauthlib import OAuth1

#This method will call our helper function to get the Twitter Paylaod and then parse it as needed
async def getTwitterUserData(auth_key, auth_secret):
    try:
        response = await twitter_user_data_call(auth_key, auth_secret)
    except:
        return Response("Bad Request", status=400)
    
    if response['status_code'] != 200:
        return Response("ERROR", status=response['status_code'])
    else:
        #Recall that our response object has all the pertinent data
        response['status_message'] = "OK"
        return jsonify(response)


######################## Helper Functions ########################

#Helper function to directly ping Twitter API to get User Payload
async def twitter_user_data_call(auth_key, auth_secret):
    endpoint_url = 'https://api.twitter.com/2/users/me'

    params = {
        "user.fields": "created_at,profile_image_url,public_metrics"
    }

    oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"),
                   resource_owner_key=auth_key, resource_owner_secret=auth_secret,
            )
    
    response = requests.get(url=endpoint_url, params=params, auth=oauth)

    #Respond with our new object
    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:

        #Parse our response
        dictionary = json.loads(response.text)['data']
        response_object['username'] = dictionary['username']
        response_object['profile_image_url'] = dictionary['profile_image_url']
        response_object['followers_count'] = dictionary['public_metrics']['followers_count']
        response_object['following_count'] = dictionary['public_metrics']['following_count']
        response_object['tweet_count'] = dictionary['public_metrics']['tweet_count']
        response_object['created_at'] = dictionary['created_at'][0:10]

        #Save the username and Id as session variables
        session['twitter_username'] =  dictionary['username']
        session['twitter_id'] = dictionary['id']
    return response_object