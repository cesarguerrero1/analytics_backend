'''
Cesar Guerrero
09/19/23

The Twitter Dashboard Controller is what will be handling all of the HTTP Endpoints once a user has been authorized.

'''

import os
from flask import (request, Blueprint, session, Response)
from ..services import twitch_dashboard_service

#Creating our blueprint so we can register with the application
bp = Blueprint('twitch_dashboard', __name__)

#Attempt to get User Data about the Twitch User
@bp.route('/dashboard/twitch/users')
async def dashboard_user_data():
    response = await twitch_dashboard_service.getTwitchUserData(session['twitch_access_token'], os.getenv("TWITCH_API_KEY"))
    return response

#Attempt to get the Bits Leaderboard for the given Twitch User
@bp.route('/dashboard/twitch/bits')
async def dashboard_bits_data():
    response = await twitch_dashboard_service.getTwitchBitsData(session['twitch_access_token'], os.getenv("TWITCH_API_KEY"))
    return response

#Attempt to get data regarding the Users Followers on Twitch
@bp.route('/dashboard/twitch/followers')
async def dashboard_followers_data():
    twitch_id = request.args.get('id')
    if twitch_id == None:
        return Response("Bad Request", status=400)
    
    response = await twitch_dashboard_service.getTwitchFollowersData(twitch_id, session['twitch_access_token'], os.getenv("TWITCH_API_KEY"))
    return response

#Attempt to get data regarding the users Subscribers on Twitch
@bp.route('/dashboard/twitch/subscribers')
async def dashboard_subscribers_data():
    twitch_id = request.args.get('id')
    if twitch_id == None:
        return Response("Bad Request", status=400)

    response = await twitch_dashboard_service.getTwitchSubscriberData(twitch_id, session['twitch_access_token'], os.getenv("TWITCH_API_KEY"))
    return response

#Attempt to get video data for all the VODs a Twitch User has archived
@bp.route('/dashboard/twitch/videos')
async def dashboard_video_data():
    twitch_id = request.args.get('id')
    if twitch_id == None:
        return Response("Bad Request", status=400)
    
    response = await twitch_dashboard_service.getTwitchVideoData(twitch_id, session['twitch_access_token'], os.getenv("TWITCH_API_KEY"))
    return response