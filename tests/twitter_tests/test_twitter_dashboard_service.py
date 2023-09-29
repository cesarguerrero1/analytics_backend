'''

Cesar Guerrero
09/28/23

Testing our Twitter Dashboard Service

'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch
from analytics_api.services import twitter_dashboard_service

class TestClassGetTwitterUser:

    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_dashboard_service.twitter_user_data_call', new=AsyncMock(return_value={
        "status_code": 200,
        "payload":
            {"id":"123123","created_at":"2013-12-14T04:35:55.000Z",
             "profile_image_url":"url-goes-here","username":"my-username",
             "public_metrics":
                {"followers_count":200,
                 "following_count":50,
                 "tweet_count":342}
             }
        }))
    async def test_get_twitter_user_success(self, client):
        with client:
            client.get('/profile')
            response = await twitter_dashboard_service.getTwitterUserData('auth-key', 'auth-secret')
            #Assert the session and the response
            assert session['twitter_username'] == "my-username"
            assert session['twitter_id'] == "123123"
            assert response.data == b'{"created_at":"2013-12-14","followers_count":200,"following_count":50,"profile_image_url":"url-goes-here","status_code":200,"status_message":"OK","tweet_count":342,"username":"my-username"}\n'
    
    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_dashboard_service.twitter_user_data_call', new=AsyncMock(return_value={"status_code":401}))
    async def test_get_twitter_user_fail(self):
        #Mock our Twitter API call
        response = await twitter_dashboard_service.getTwitterUserData('auth-key', 'auth-secret')
        assert response.status_code == 401
        assert response.data == b'ERROR'


    @pytest.mark.asyncio
    @patch('analytics_api.services.twitter_dashboard_service.twitter_user_data_call', new=AsyncMock())
    async def test_get_twitter_user_error(self):
        #We are simulating an error with the request. By not including a JSON, for a successful 
        #API call, we can force our code to throw an exception
        response = await twitter_dashboard_service.getTwitterUserData('auth-key', 'auth-secret')
        assert response.status_code == 400
        assert response.data == b'Bad Request'
    