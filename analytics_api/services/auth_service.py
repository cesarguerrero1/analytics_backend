'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import sys
import oauth2 as oauth
import urllib
import httpx
from flask import session

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'

    try:
        consumer = oauth.Consumer(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        client = oauth.Client(consumer)
        response, content = client.request(endpoint_url, "POST", body=urllib.parse.urlencode({"oauth_callback": os.getenv("CALLBACK_URI")}))
        request_token = dict(urllib.parse.parse_qsl(content))
        
        if response['status'] != '200':
            return False

        session['oauth_token'] = request_token[b'oauth_token'].decode('utf-8')
        session['oauth_token_secret'] = request_token[b'oauth_token_secret'].decode('utf-8')
        print(session)
        sys.stdout.flush()
        return True
    
    except:
        #We failed the first-leg of OAuth1.0
        return False

#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'

    try:
        consumer = oauth.Consumer(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        token = oauth.Token(session_token, session_secret)
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        response, content = client.request(endpoint_url, "POST")
        access_token = dict(urllib.parse.parse_qsl(content))
        
        #Store these now verified keys in the session for future API calls
        session['auth_key'] = access_token[b'oauth_token'].decode('utf-8')
        session['auth_secret'] = access_token[b'oauth_token_secret'].decode('utf-8')
        session['username'] = access_token[b'screen_name'].decode('utf-8')
        session['user_id'] = access_token[b'user_id'].decode('utf-8')

        return True
    except:
        return False