'''
Cesar Guerrero
08/24/23

Base Authentication Controller to handle whether a user is logged in and when to log them out

'''
from flask import (Blueprint, session, jsonify)

#Creating our blueprint so we can register with the application
bp = Blueprint('auth', __name__)

#Check if the user is logged in.
@bp.route('/profile')
def profile():
    return is_logged_in(session.get('is_logged_in', None))

#Destroy the session
@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'status_code': 200, 'status_message': "OK", "session_destroyed": True})


############# HELPER FUNCTIONS #############

#Function to check whether a user is logged in. It will set some session key-values if no user is found
def is_logged_in(logged_in):
    if logged_in == True:
        #A session exists for the given user
        return jsonify({'status_code': 200, 'status_message': "OK", "is_logged_in": True, "app": session.get('app')})
    else:
        #A session does not exist for the given user
        session['is_logged_in'] = False
        session['app'] = None
        return jsonify({'status_code': 200, 'status_message': "OK", "is_logged_in": False, "app": None})