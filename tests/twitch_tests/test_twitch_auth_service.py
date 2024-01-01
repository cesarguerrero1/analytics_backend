'''
Cesar Guerrero
09/27/23

Testing our Twitch Authorization Service file
'''
import pytest
import responses
from flask import session
from analytics_api.services import twitch_auth_service


class TestClassAuthorization:

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitch_access_token_pass(self, client):
        
        #Mock our API call
        responses.post(
            url='https://id.twitch.tv/oauth2/token',
            body='{"access_token":"access123","refresh_token":"ref123"}',
            status=200
        )

        with client:
            client.get('/profile')
            response = await twitch_auth_service.obtain_twitch_access_token("code123")
            assert session['twitch_access_token'] == 'access123'
            assert session['twitch_refresh_token'] == 'ref123'
            assert session['is_logged_in'] == True
            assert session['app'] == "Twitch"
            assert response.data == b'{"oauth_approved":true,"status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitch_access_token_fail(self):
        #Mock our API call
        responses.post(
            url='https://id.twitch.tv/oauth2/token',
            body='Unauthorized',
            status=401
        )
        response = await twitch_auth_service.obtain_twitch_access_token("code123")
        assert response.status_code == 401
        assert response.data == b'ERROR'

    @pytest.mark.asyncio
    @responses.activate
    async def test_obtain_twitch_access_token_error(self):
        #Mock our API call
        responses.post(
            url='https://id.twitch.tv/oauth2/token',
            status=200
        )
        response = await twitch_auth_service.obtain_twitch_access_token("code123")
        assert response.status_code == 400
        assert response.data == b'Bad Request'
    
