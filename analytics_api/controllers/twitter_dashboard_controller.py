'''
Cesar Guerrero
09/19/23

The Twitter Dashboard Controller is what will be handling all of the HTTP Endpoints once a user has been authorized.

'''

from flask import (Blueprint, session, Response)
from ..services import twitter_dashboard_service

#Creating our blueprint so we can register with the application
bp = Blueprint('twitter_dashboard', __name__)

#Attempt to get User Data about the authorized User
@bp.route('/dashboard/twitter/users')
async def dashboard_user_data():
    #Grab our session data so we can ping the Twitter server
    response = await twitter_dashboard_service.getTwitterUserData(session['twitter_auth_key'], session['twitter_auth_secret'])
    return response

#Attempt to get Tweet Data about the authorized User
@bp.route('/dashboard/twitter/tweets')
async def dashboard_tweet_data():
    return Response("No Data", 200)
