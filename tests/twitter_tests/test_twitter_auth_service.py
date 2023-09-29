'''
Cesar Guerrero
09/27/23

Testing our Twitter Authorization Service file
'''
import pytest
from flask import session
from unittest.mock import AsyncMock, patch
from analytics_api.services import twitter_auth_service

class TestClassRequest:

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_request_call',
           new=AsyncMock(return_value={"status_code": 200, "oauth_token": "abc", "oauth_token_secret": "123"}))
    async def test_obtain_twitter_request_token_pass(self, client):

        #This function accesses our session so we need to start one via '/profile'
        with client:
            client.get('/profile')
            response = await twitter_auth_service.obtain_twitter_request_token()
            assert session['twitter_oauth_token'] == 'abc'
            assert session['twitter_oauth_token_secret'] == '123'
            assert response.data == b'{"oauth_ready":true,"oauth_token":"abc","status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_request_call', new=AsyncMock(return_value={"status_code":401}))
    async def test_obtain_twitter_request_token_fail(self):

        #No need for sessions as the code will not get that far
        response = await twitter_auth_service.obtain_twitter_request_token()
        assert response.status_code == 401
        assert response.data == b'ERROR'
    
    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_request_call', new=AsyncMock())
    async def test_obtain_twitter_request_token_error(self):
        #We are simulating an error with the request. By not including a body, for a successful 
        #API call, we can force our code to throw an exception
        response = await twitter_auth_service.obtain_twitter_request_token()
        assert response.status_code == 400
        assert response.data == b'Bad Request'


class TestClassAuthorization:

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_authorization_call',
           new=AsyncMock(return_value={"status_code": 200, "twitter_auth_key": "123abc", "twitter_auth_secret": "456def"}))
    async def test_obtain_twtter_access_token_pass(self, client):

        #This function accesses our session so we need to start one via '/profile'
        with client:
            client.get('/profile')
            response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
            assert session['twitter_auth_key'] == '123abc'
            assert session['twitter_auth_secret'] == '456def'
            assert session['is_logged_in'] == True
            assert session['app'] == "Twitter"
            assert response.data == b'{"oauth_approved":true,"status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_authorization_call', new=AsyncMock(return_value={"status_code":401}))
    async def test_obtain_twtter_access_token_fail(self):
        response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
        assert response.status_code == 401
        assert response.data == b'ERROR'

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_auth_service.twitter_authorization_call', new=AsyncMock())
    async def test_obtain_twtter_access_token_error(self):
        response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
        assert response.status_code == 400
        assert response.data == b'Bad Request'
