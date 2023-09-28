'''
Cesar Guerrero
08/24/23

The Twitch Dashboard Service is how we interact with the Twitch API for Dashboard services.
We will be curating all the data here before returning it to the controller.

'''
import httpx #Library to make async HTTP requests
from flask import (session, Response, jsonify)

#Call the Twitch API to get our User Payload
async def getTwitchUserData(access_token, client_id):
    try:
        header = {
            "Authorization": "Bearer %s" %access_token,
            "Client-Id": client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.twitch.tv/helix/users", headers=header)
    except:
        return Response("Bad Request", status=400)
    
    response_object = {}
    response_object['status_code'] = response.status_code

    if response_object['status_code'] == 200:
        response_object['status_message'] = "OK"

        #Parse Response
        payload = response.json()['data'][0]
        response_object['created_at'] = payload['created_at'][0:10]
        response_object['profile_image_url'] = payload['profile_image_url']
        response_object['twitch_id'] = payload['id']
        response_object['username'] = payload['display_name']

        #Save the id and username as session variables
        session['twitch_id'] = payload['id']
        session['twitch_username'] = payload['display_name']
    else:
        return Response("ERROR", status=response['status_code'])

    return jsonify(response_object)

#Call the Twitch API to get our Bits Leaderboard Payload
async def getTwitchBitsData(access_token, client_id):
    try:
        header = {
            "Authorization": "Bearer %s" %access_token,
            "Client-Id": client_id
        }
        async with httpx.AsyncClient() as client:
            #By default this will return the top 10 people who have given Bits to the stream
            response = await client.get("https://api.twitch.tv/helix/bits/leaderboard", headers=header)
    except:
        return Response("Bad Request", status=400)

    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        response_object['status_message'] = "OK"

        #Parse Response
        data_array = response.json()['data']
        if(len(data_array) > 0):
            #We only care about the score
            rank_array = []
            for item in data_array:
                rank_array.append([item['user_name'], item['score']])
            response_object['bits_array'] = rank_array
        else:
            #This will just be an empty array
            response_object['bits_array'] = data_array
            
    else:
        return Response("ERROR", status=response['status_code'])

    return jsonify(response_object)

#Call the Twitch API to get our Followers Payload
async def getTwitchFollowersData(broadcaster_id, access_token, client_id):
    try:
        params = {
            'broadcaster_id': broadcaster_id
        }

        header = {
            "Authorization": "Bearer %s" %access_token,
            "Client-Id": client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.twitch.tv/helix/channels/followers", params=params, headers=header)
    except:
        return Response("Bad Request", status=400)

    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        response_object['status_message'] = "OK"

        #Parse Response
        payload = response.json()
        response_object['followers'] = payload['total'] 
    else:
        return Response("ERROR", status=response['status_code'])
    return jsonify(response_object)

#Call the Twitch API to get our Subscribers Payload
async def getTwitchSubscriberData(broadcaster_id, access_token, client_id):
    #Data holder
    response_object = {}

    try:
        params = {
            'broadcaster_id': broadcaster_id,
            'first': '100',
        }

        header = {
            "Authorization": "Bearer %s" %access_token,
            "Client-Id": client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.twitch.tv/helix/subscriptions", params=params, headers=header)

            response_object['status_code'] = response.status_code
            if response_object['status_code'] == 200:
                response_object['status_message'] = "OK"

                #Parse the response
                payload = response.json()

                response_object['subscriber_points'] = payload['points']
                response_object['subscribers'] = payload['total']
                response_object['subscriber_tiers_array'] = [0,0,0]
                #Now we need to loop over all of our subscribers
                while True:
                    for subscriber in payload['data']:
                        if(subscriber['tier'] == '1000'):
                            response_object['subscriber_tiers_array'][0] += 1
                        elif(subscriber['tier'] == '2000'):
                             response_object['subscriber_tiers_array'][1] += 1
                        else:
                             response_object['subscriber_tiers_array'][2] += 1
                    #Now we need to see if there is another page
                    cursor = payload['pagination'].get("cursor", None)
                    if(cursor == None):
                        break
                    else:
                        params['after'] = cursor
                        #Call the next page and run the loop again
                        response = await client.get("https://api.twitch.tv/helix/subscriptions", params=params, headers=header)
                        payload = response.json()
            else:
                return Response("ERROR", status=response['status_code'])
    except:
        return Response("Bad Request", status=400)
    return jsonify(response_object)

#Call the Twitch API to get our Video Payload
async def getTwitchVideoData(broadcaster_id, access_token, client_id):
    try:
        params = {
            'user_id': broadcaster_id,
            'type': 'archive',
            'first': '100',
        }

        header = {
            "Authorization": "Bearer %s" %access_token,
            "Client-Id": client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.twitch.tv/helix/videos", params=params, headers=header)
    except:
        return Response("Bad Request", status=400)
    
    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        response_object['status_message'] = "OK"
        payload = response.json()

        #We only care about the first 10 videos so no need to paginate
        video_array = payload['data']
        if(len(video_array) > 0 ):
            #We only care about the score
            rank_array = []
            for video in video_array:
                #The order will be from most recent to oldest
                rank_array.append([video['view_count'], video['duration']])
            response_object['video_array'] = rank_array
        else:
            #This will be an empty array
            response_object['video_array'] = video_array
    else:
        return Response("ERROR", status=response['status_code'])
    return jsonify(response_object)
