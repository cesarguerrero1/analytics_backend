'''
Cesar Guerrero
08/24/23

The Twitter Dashboard Service is how we interact with the Twitter API for Dashboard services
We will be curating all the data here before returning it to the controller.

'''

import os
import requests
from flask import (json, session, Response, jsonify, current_app)
from requests_oauthlib import OAuth1

#This method will call our helper function to get the Twitter Paylaod and then parse it as needed
async def getTwitterUserData(auth_key, auth_secret):
    try:
        response = await twitter_user_data_call(auth_key, auth_secret)
    
        return response

    except:
        return Response("Bad Request", status=400)
    

######################## Helper Functions ########################

#Helper function to directly ping Twitter API to get User Payload
async def twitter_user_data_call(auth_key, auth_secret):
    endpoint_url = 'https://api.twitter.com/2/users/me'

    params = {
        "user.fields": "created_at,profile_image_url,public_metrics"
    }
    #Checking to see if we can just circumnavigate this in testing
    if current_app.config['TESTING'] == True:
        response = requests.get(url=endpoint_url, params=params)
    else:
        oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"),
                resource_owner_key=auth_key, resource_owner_secret=auth_secret,
        )
        response = requests.get(url=endpoint_url, params=params, auth=oauth)

    response_object = {}
    if response.status_code == 200:
        response_object['status_code'] = 200
        response_object['status_message'] = "OK"

        dictionary = json.loads(response.text)['data']
        response_object['created_at'] = dictionary['created_at'][0:10]
        response_object['followers_count'] = dictionary['public_metrics']['followers_count']
        response_object['following_count'] = dictionary['public_metrics']['following_count']
        response_object['profile_image_url'] = dictionary['profile_image_url']
        response_object['tweet_count'] = dictionary['public_metrics']['tweet_count']
        response_object['username'] = dictionary['username']

        #Save the username and Id as session variables
        session['twitter_username'] =  dictionary['username']
        session['twitter_id'] = dictionary['id']

        return jsonify(response_object)
    else:
        return Response("ERROR", status=response.status_code)
