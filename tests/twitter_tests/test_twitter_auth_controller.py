'''
Cesar Guerrero
09/27/23

Testing our Twitter Authorization Controller
'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch

'''
#Testing the login Route
class TestLoginClass:

    @patch('analytics_api.services.auth_service.obtain_twitter_request_token', new=AsyncMock(return_value={"status_code": 200, "status_message":"OK", "oauth_token": "abc"}))
    def test_login_good_response(self,client):
        #You should not be able to call login with anything other than GET
        assert client.post('/login').status_code == 405
        assert client.get('/login').status_code == 200
        response = client.get('/login')
        assert response.data == b'{"oauth_ready":true,"oauth_token":"abc","status_code":200,"status_message":"OK"}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_request_token', new=AsyncMock(return_value={"status_code": 401, "status_message": "Unauthorized"}))
    def test_login_bad_response(self,client):
        response = client.get('/login')
        assert response.data == b'{"oauth_ready":false,"status_code":401,"status_message":"Unauthorized"}\n'



#Testing the Callback Route
class TestCallbackClass:
    
    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={"status_code": 200, "status_message":"OK", "current_user": 'me'}))
    def test_callback_good_response(self,client):
        with client.session_transaction() as session:
            session['oauth_token'] = "abc123" #Setting up a session variable
            session['oauth_token_secret'] = '?'
        response = client.get('/callback/twitter?oauth_token=%s&oauth_verifier=%s' %("abc123", "789xyz"))
        assert response.data == b'{"current_user":"me","oauth_approved":true,"status_code":200,"status_message":"OK"}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={"status_code": 401, "status_message": "Unauthorized"}))
    def test_callback_bad_response(self,client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['oauth_token'] = "abc123" 
            session['oauth_token_secret'] = '?'
        response = client.get('/callback/twitter?oauth_token=%s&oauth_verifier=%s' %("abc123", "789xyz"))
        assert response.data == b'{"current_user":null,"oauth_approved":false,"status_code":401,"status_message":"Unauthorized"}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock())
    def test_callback_token_mismatch(self,client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['oauth_token'] = "abc123"
            session['oauth_token_secret'] = '?'
        response = client.get('/callback/twitter?oauth_token=%s&oauth_verifier=%s' %("abc124", "789xyz"))
        assert response.data == b'{"current_user":null,"oauth_approved":false,"status_code":401,"status_message":"Unauthorized"}\n' #Mismatch of tokens even though we have a good response
'''