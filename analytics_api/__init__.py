'''
Cesar Guerrero
08/24/23

This file serves as our 'Application Factory'. Depending on the environment, we should be doing different things!
'''

import os
import logging
import redis
from flask import Flask
from flask_session import Session
from flask_cors import CORS

#Controllers 
from .controllers import (auth_controller, dashboard_controller)

#We are creating our Flask Server
def create_app():
    app = Flask(__name__)

    #Heroku Logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    #We do not want to use Flask's built-in session
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_TYPE']='redis'

    if os.getenv("ENVIRONMENT") == "PRODUCTION":
        #Set our Secret Key if we are in production
        app.config.from_mapping(
            #Get environmental variables from Heroku
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SESSION_COOKIE_HTTPONLY=False, #Default is True
            SESSION_COOKIE_SECURE=True, #Defaul is False
            SESSION_PERMANENT=False,
            SESSION_REDIS=redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"))
        )
        cors = CORS(app, origins=[os.getenv("FRONT_END_URL")], supports_credentials=True)
    else:
        #We are in production so just setting a dummy variable
        app.config.from_mapping(
            SECRET_KEY="dev",
            SESSION_REDIS=redis.Redis(host='localhost', port=6379)
        )
        cors = CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    Session(app)


    #Register all of our controllers
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(dashboard_controller.bp)

    return app