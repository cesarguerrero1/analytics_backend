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
from .controllers import (auth_controller, dashboard_controller)

#We are creating our Flask Server
def create_app(environment = None):
    app = Flask(__name__)

    #Depending on the environment, deploy different settings
    factory(environment, app)

    #Activate Sessions and CORS
    Session(app)
    CORS(app, origins=[os.getenv("FRONT_END_URL")], supports_credentials=True)


    #Register all of our controllers
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(dashboard_controller.bp)

    return app

#Create a different factory based on our instance type
def factory(factoryInstanceType, app):
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
            SESSION_REDIS=redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"))
        )
    else:
        app.config['SESSION_REDIS']=redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
        app.config['SESSION_COOKIE_HTTPONLY'] = False
        if factoryInstanceType == "DEV":
            app.config.from_mapping(
                SECRET_KEY='dev',
            )

        elif factoryInstanceType == "TESTING":
            app.config.from_mapping(
                SECRET_KEY='test',
                TESTING=True
            )
    return 