'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import requests
import httpx
from requests_oauthlib import OAuth1
from flask import session

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'

    #NOTE: Potential issue.. YOu cannot AWAIT the oauth for some reason...
    oauth = OAuth1(client_key=os.getenv("API_KEY"), client_secret=os.getenv("API_SECRET"), callback_uri=os.getenv("CALLBACK_URI"))
    response = requests.post(endpoint_url, auth=oauth)

    if response.status_code == 200:
        parameters = response.text.split("&")
        for text in parameters:
            key_value = text.split("=")
            session[key_value[0]] = key_value[1]
    return