'''
Cesar Guerrero
09/27/23

Testing our Twitter Authorization Service file
'''
import pytest
import responses
from flask import session
from analytics_api.services import twitter_auth_service

'''
class TestClassRequest:

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitter_request_token_pass(self, client):
        #Mock the call to Twitter API
        responses.get(
            url='https://api.twitter.com/oauth/request_token',
            body='oauth_token=abc123&oauth_token_secret=xyz456',
            status=200
        )

        #This function accesses our session so we need to start one via '/profile'
        with client:
            client.get('/profile')
            response = await twitter_auth_service.obtain_twitter_request_token()
            assert session['twitter_oauth_token'] == 'abc123'
            assert session['twitter_oauth_token_secret'] == 'xyz456'
            assert response.data == b'{"oauth_ready":true,"oauth_token":"abc123","status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitter_request_token_fail(self):
        #Mock the call to Twitter API
        responses.get(
            url='https://api.twitter.com/oauth/request_token',
            body='Unauthorized',
            status=401
        )

        #No need for sessions as the code will not get that far
        response = await twitter_auth_service.obtain_twitter_request_token()
        assert response.status_code == 401
        assert response.data == b'ERROR'
    
    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitter_request_token_error(self):
        #Mock the call to Twitter API
        responses.get(
            url='https://api.twitter.com/oauth/request_token',
            status=200
        )

        #We are simulating an error with the request. By not including a body, for a successful 
        #API call, we can force our code to throw an exception
        response = await twitter_auth_service.obtain_twitter_request_token()
        assert response.status_code == 400
        assert response.data == b'Bad Request'


class TestClassAuthorization:

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twtter_access_token_pass(self, client):
        #Mock Twitter API Call
        responses.post(
            url='https://api.twitter.com/oauth/access_token',
            body='oauth_token=auth123&oauth_token_secret=authsecret456',
            status=200
        )

        #This function accesses our session so we need to start one via '/profile'
        with client:
            client.get('/profile')
            response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
            assert session['twitter_auth_key'] == 'auth123'
            assert session['twitter_auth_secret'] == 'authsecret456'
            assert session['is_logged_in'] == True
            assert session['app'] == "Twitter"
            assert response.data == b'{"oauth_approved":true,"status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twtter_access_token_fail(self):
        #Mock Twitter API Call
        responses.post(
            url='https://api.twitter.com/oauth/access_token',
            body='Unauthorized',
            status=401
        )

        response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
        assert response.status_code == 401
        assert response.data == b'ERROR'

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twtter_access_token_error(self):
        #Mock Twitter API Call
        responses.post(
            url='https://api.twitter.com/oauth/access_token',
            status=200
        )

        response = await twitter_auth_service.obtain_twitter_access_token('verifier', 'token', 'secret')
        assert response.status_code == 400
        assert response.data == b'Bad Request'
'''
