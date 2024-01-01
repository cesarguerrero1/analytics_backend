'''
Cesar Guerrero
09/27/23

Testing the Twitch Dashboard Controller

'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch

class TestClassUserPayload:

    @patch('analytics_api.services.twitch_dashboard_service.getTwitchUserData',
           new=AsyncMock(return_value={"created_at":"some-date-here", "profile_image_url":"url-goes-here", 
                                       "status_code":200, "status_message":"OK", "twitch_id":"my-twitch-id", 
                                       "username":"twitch-username"}))
    def test_user_payload(self,client):
        with client.session_transaction() as session:
            session['twitch_access_token'] = 'twitch123'
        response = client.get('/dashboard/twitch/users')
        assert response.status_code == 200
        assert response.data == b'{"created_at":"some-date-here","profile_image_url":"url-goes-here","status_code":200,"status_message":"OK","twitch_id":"my-twitch-id","username":"twitch-username"}\n'

class TestClassBitsPayload:
    
    @patch('analytics_api.services.twitch_dashboard_service.getTwitchBitsData', 
           new=AsyncMock(return_value={"bits_array":[["user1", 150], ["user2", 100], ["user3", 90]], "status_code":200, "status_message": "OK"}))
    def test_bits_payload(self,client):
        with client.session_transaction() as session:
            session['twitch_access_token'] = 'twitch123'
        response = client.get('/dashboard/twitch/bits')
        assert response.status_code == 200
        assert response.data == b'{"bits_array":[["user1",150],["user2",100],["user3",90]],"status_code":200,"status_message":"OK"}\n'

class TestClassFollowersPayload:
    
    def test_followers_payload_null_twitchId(self, client):
        response = client.get('/dashboard/twitch/followers')
        assert response.status_code == 401
        assert response.data == b'Unauthorized'

    @patch('analytics_api.services.twitch_dashboard_service.getTwitchFollowersData', 
           new=AsyncMock(return_value={"followers":43, "status_code":200, "status_message": "OK"}))
    def test_followers_payload(self,client):
        with client.session_transaction() as session:
            session['twitch_access_token'] = 'twitch123'
        response = client.get('/dashboard/twitch/followers?id=twitchId123')
        assert response.status_code == 200
        assert response.data == b'{"followers":43,"status_code":200,"status_message":"OK"}\n'

class TestClassSubscribersPayload:

    def test_subscribers_payload_null_twitchId(self, client):
        response = client.get('/dashboard/twitch/subscribers')
        assert response.status_code == 401
        assert response.data == b'Unauthorized'
    
    @patch('analytics_api.services.twitch_dashboard_service.getTwitchSubscriberData', 
           new=AsyncMock(return_value={"status_code":200, "status_message": "OK", "subscribers":354, "subscriber_points":1042, "subscriber_tiers_array":[21,45,13]}))
    def test_subscribers_payload(self,client):
        with client.session_transaction() as session:
            session['twitch_access_token'] = 'twitch123'
        response = client.get('/dashboard/twitch/subscribers?id=twitchId123')
        assert response.status_code == 200
        assert response.data == b'{"status_code":200,"status_message":"OK","subscriber_points":1042,"subscriber_tiers_array":[21,45,13],"subscribers":354}\n'

class TestClassVideosPayload:

    def test_videos_payload_null_twitchId(self, client):
        response = client.get('/dashboard/twitch/videos')
        assert response.status_code == 401
        assert response.data == b'Unauthorized'

    @patch('analytics_api.services.twitch_dashboard_service.getTwitchVideoData', 
           new=AsyncMock(return_value={"video_array":[[12323, "3m21s"], [49321, "4h22m31s"], [94234, "49m22s"]], "status_code":200, "status_message": "OK"}))
    def test_videos_payload(self,client):
        with client.session_transaction() as session:
            session['twitch_access_token'] = 'twitch123'
        response = client.get('/dashboard/twitch/videos?id=twitchId123')
        assert response.status_code == 200
        assert response.data == b'{"status_code":200,"status_message":"OK","video_array":[[12323,"3m21s"],[49321,"4h22m31s"],[94234,"49m22s"]]}\n'