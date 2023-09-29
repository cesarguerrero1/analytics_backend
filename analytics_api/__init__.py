'''
Cesar Guerrero
08/24/23

This file serves as our 'Application Factory'. Depending on the environment, we should be doing different things!
'''

import os
import redis
from flask import Flask
from flask_session import Session
from flask_cors import CORS

#Controllers
from .controllers import (auth_controller, twitter_dashboard_controller, twitter_auth_controller, twitch_dashboard_controller, twitch_auth_controller)

#We are creating our Flask Server - If no environment is found just assume we are testing
def create_app(environment = "TESTING"):
    app = Flask(__name__)

    #Depending on the environment, deploy different settings
    factory(environment, app)

    #Register all of our controllers
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(twitter_auth_controller.bp)
    app.register_blueprint(twitch_dashboard_controller.bp)
    app.register_blueprint(twitter_dashboard_controller.bp)
    app.register_blueprint(twitch_auth_controller.bp)
    

    return app

#Create a different factory based on our instance type
def factory(factoryInstanceType, app):
    if factoryInstanceType == "TESTING":
        app.config.from_mapping(
            SECRET_KEY='test',
            TESTING=True,
        )
    else:
        #Session Setting Modifications
        app.config['SESSION_USE_SIGNER'] = True
        app.config['SESSION_TYPE']='redis'
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = "None"
        app.config['SESSION_PERMANENT'] = False
        
        if factoryInstanceType == "PRODUCTION":
            app.config.from_mapping(
                SECRET_KEY=os.getenv("SECRET_KEY"),
                SESSION_COOKIE_HTTPONLY=True,
                SESSION_REDIS=redis.Redis(
                    host=os.getenv("REDIS_HOST"),
                    port=os.getenv("REDIS_PORT"), 
                    password=os.getenv("REDIS_PASSWORD")
                )
            )
        elif factoryInstanceType == "DEV":
            app.config.from_mapping(
                SECRET_KEY='dev',
                SESSION_REDIS=redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT")),
                SESSION_COOKIE_HTTPONLY=False
            )

        #Activate Sessions and CORS
        Session(app)
        CORS(app, origins=[os.getenv("FRONT_END_URL")], supports_credentials=True)
    return 