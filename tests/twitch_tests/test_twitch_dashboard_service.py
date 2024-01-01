'''

Cesar Guerrero
09/28/23

Testing our Twitch Dashboard Service

'''

import pytest
from flask import session
from pytest_httpx import HTTPXMock
from analytics_api.services import twitch_dashboard_service

class TestClassGetTwitchUser:
    
    @pytest.mark.asyncio
    async def test_get_twitch_user_data_success(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/users",
            json = {"data":
                    [
                        {
                            "id":"123123",
                            "created_at":"2016-12-14T20:32:28Z",
                            "profile_image_url":"url-goes-here",
                            "display_name":"my-username"
                        }
                    ]
                    },
            status_code=200
            )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchUserData('access-token', 'client-id')
            assert session['twitch_id'] == "123123"
            assert session['twitch_username'] == "my-username"
            assert response.data == b'{"created_at":"2016-12-14","profile_image_url":"url-goes-here","status_code":200,"status_message":"OK","twitch_id":"123123","username":"my-username"}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_user_data_fail(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/users",
            text = "Unauthorized",
            status_code=401
            )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchUserData('access-token', 'client-id')
            assert response.status_code == 401
            assert response.data == b'ERROR'

    @pytest.mark.asyncio
    async def test_get_twitch_user_data_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/users",
            text = "Unauthorized",
            status_code=200
            )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchUserData('access-token', 'client-id')
            assert response.status_code == 400
            assert response.data == b'Bad Request'

class TestClassGetTwitchBits:
    
    @pytest.mark.asyncio
    async def test_get_twitch_bits_data_success_full(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/bits/leaderboard",
            json = {"data":
                    [
                        {
                            "user_name": "TundraCowboy",
                            "rank": 1,
                            "score": 12543
                        },
                        {
                            "user_name": "Topramens",
                            "rank": 2,
                            "score": 6900
                        }
                    ]
                    },
            status_code = 200
            )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchBitsData('access-token', 'client-id')
            assert response.data == b'{"bits_array":[["TundraCowboy",12543],["Topramens",6900]],"status_code":200,"status_message":"OK"}\n'
    
    @pytest.mark.asyncio
    async def test_get_twitch_bits_data_success_empty(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/bits/leaderboard",
            json = {"data":
                    [],
                    },
            status_code = 200
            )
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchBitsData('access-token', 'client-id')
            assert response.data == b'{"bits_array":[],"status_code":200,"status_message":"OK"}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_bits_data_fail(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/bits/leaderboard",
            text = "Unauthorized",
            status_code = 401
            )
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchBitsData('access-token', 'client-id')
            assert response.status_code == 401
            assert response.data == b'ERROR'

    @pytest.mark.asyncio
    async def test_get_twitch_bits_data_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/bits/leaderboard",
            text = "Unauthorized",
            status_code = 200
            )
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchBitsData('access-token', 'client-id')
            assert response.status_code == 400
            assert response.data == b'Bad Request'

class TestClassGetTwitchFollowers:

    @pytest.mark.asyncio
    async def test_get_twitch_followers_data_success(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/channels/followers?broadcaster_id=broadcaster-id",
            json = {"total":8},
            status_code = 200
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchFollowersData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"followers":8,"status_code":200,"status_message":"OK"}\n'
    
    @pytest.mark.asyncio
    async def test_get_twitch_followers_data_fail(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/channels/followers?broadcaster_id=broadcaster-id",
            text = "Unauthorized",
            status_code = 401
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchFollowersData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 401
            assert response.data == b'ERROR'

    @pytest.mark.asyncio
    async def test_get_twitch_followers_data_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/channels/followers?broadcaster_id=broadcaster-id",
            text = "Unauthorized",
            status_code = 200
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchFollowersData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 400
            assert response.data == b'Bad Request'

class TestClassGetTwitchSubscribers:

    @pytest.mark.asyncio
    async def test_get_twitch_subscribers_data_success_full(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100",
            json = {"data":
                    [
                        {
                            "user_name": "TundraCowboy",
                            "tier":"2000"
                        },
                        {
                            "user_name": "Topramens",
                            "tier":"3000"
                        }
                    ],
                    "pagination":{},
                    "total":2340,
                    "points":12390
                    },
            status_code = 200
        )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchSubscriberData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"status_code":200,"status_message":"OK","subscriber_points":12390,"subscriber_tiers_array":[0,1,1],"subscribers":2340}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_subscribers_data_success_empty(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100",
            json = {"data":
                    [],
                    "pagination":{},
                    "total":0,
                    "points":12390
                    },
            status_code = 200
        )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchSubscriberData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"status_code":200,"status_message":"OK","subscriber_points":12390,"subscriber_tiers_array":[0,0,0],"subscribers":0}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_subscribers_data_success_pagination(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100",
            json = {"data":
                    [
                        {
                            "user_name": "TundraCowboy",
                            "tier":"2000"
                        },
                        {
                            "user_name": "Topramens",
                            "tier":"3000"
                        }
                    ],
                    "pagination":{
                        "cursor":"cursor-id"
                    },
                    "total":2340,
                    "points":12390
                    },
            status_code = 200
        )
        #Second call for pagination
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100&after=cursor-id",
            json = {"data":
                    [
                        {
                            "user_name": "CowboyTundra",
                            "tier":"3000"
                        },
                        {
                            "user_name": "RamenTop",
                            "tier":"1000"
                        }
                    ],
                    "pagination":{},
                    #While these are included we will never interact with them after the first call hence why I put new
                    #numbers to just double check
                    "total":23,
                    "points":12
                    },
            status_code = 200
        )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchSubscriberData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"status_code":200,"status_message":"OK","subscriber_points":12390,"subscriber_tiers_array":[1,1,2],"subscribers":2340}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_subscribers_data_fail(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100",
            text="Unauthorized",
            status_code = 401
        )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchSubscriberData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 401
            assert response.data == b'ERROR'

    @pytest.mark.asyncio
    async def test_get_twitch_subscribers_data_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/subscriptions?broadcaster_id=broadcaster-id&first=100",
            text="Unauthorized",
            status_code = 200
        )

        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchSubscriberData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 400
            assert response.data == b'Bad Request'

class TestClassGetTwitchVideos:

    @pytest.mark.asyncio
    async def test_get_twitch_videos_data_success_full(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/videos?first=100&type=archive&user_id=broadcaster-id",
            json = {
                "data":[
                    {
                        "title": "Twitch Developers 101",
                        "view_count": 1863062,
                        "duration": "3m21s",
                    },
                    {
                        "title": "Twitch Developers 202",
                        "view_count": 2343062,
                        "duration": "5m05s",
                    }
                ]
            },
            status_code = 200
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchVideoData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"status_code":200,"status_message":"OK","video_array":[[1863062,"3m21s"],[2343062,"5m05s"]]}\n'
    
    @pytest.mark.asyncio
    async def test_get_twitch_videos_data_success_empty(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/videos?first=100&type=archive&user_id=broadcaster-id",
            json = {
                "data":[]
            },
            status_code = 200
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchVideoData('broadcaster-id', 'access-token', 'client-id')
            assert response.data == b'{"status_code":200,"status_message":"OK","video_array":[]}\n'

    @pytest.mark.asyncio
    async def test_get_twitch_videos_data_fail(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/videos?first=100&type=archive&user_id=broadcaster-id",
            text="Unauthorized",
            status_code = 401
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchVideoData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 401
            assert response.data == b'ERROR'

    @pytest.mark.asyncio
    async def test_get_twitch_videos_data_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.twitch.tv/helix/videos?first=100&type=archive&user_id=broadcaster-id",
            text="Unauthorized",
            status_code = 200
        )
        
        with client:
            client.get('/profile')
            response = await twitch_dashboard_service.getTwitchVideoData('broadcaster-id', 'access-token', 'client-id')
            assert response.status_code == 400
            assert response.data == b'Bad Request'