# Analytics Website Backend

## Overview
This repository contains all of the files needed to run the backend for the Analytics website that I have created.

The purpose of the Analytics website is to showcase an Oauth1 and Oauth2 workflow for Twitter and Twitch, respectively. The user will be able to perform a "single-click" authentication process with their login information from either of those websites. Upon successful login, a dashboard containing metrics pertaining to either Twitter or Twitch for the user will be displayed using appropriate charts and graphs.

Website Link: https://resplendent-mousse-173f05.netlify.app/dashboard

## Architecture & Design Ideas
The architecture and design ideas are as follows:
1. For this project I decided to use a MVC (Model-View-Controller) Architecture along with Factory and Decorator Design Patterns.
    - The Factory design pattern was used to allow the backend to be deployed in different environments. When the program is first started it attempts to retrieve an environmental variable to determine the deployment environment (development, testing, production) so that specific settings can be set before the server begins to accept connections.
    - The Decorator design pattern was used mainly to associate http endpoints with the functions that would run the server logic
2. I chose to use Flask because it is lightweight and does not force you to follow any predefined rules or template.
3. The server is currently being hosted on Heroku for ease of deployment, but it can easily be hosted on Google Cloud/AWS/DigitalOcean/Etc.
4. Heroku requires the use of Github for continuous deployment, so I went a step further to establish a CI/CD pipeline using Github Actions and pytest.
    - Anytime a Pull Request is made on the "main" or "develop" branch, a Github Actions workflow is automatically started and a suite of unit tests are run against the codebase before a merge can occur. Once the PR is approved on the main branch, Heroku automatically deploys the changes on the production server.


## Testing
All of the tests can be found in the "./tests" folder and tests can be run by using the "coverage run -m pytest" command. The results of all of the tests will be outputted to the console, and you can see a coverage report using the command "coverage report".

Testing is handled using Pytest, and as mentioned before, tests are automatically run by Github Actions when a PR is made to the "develop" or "main" branch. For each unit test I tried to isolate functions as much as possible and mocked any calls to external APIs as needed.

Tests were also performed manually using Postman API as needed. It proved very useful when programming errors arose as it allowed me to verify whether I was making a valid or invalid programmatic call to the APIs for Twitter and Twitch. 


## How to run this program locally
1. Clone the repository
2. Create and activate a virtual Python environment using the Python version found in runtime.txt
3. Use the following command to install all the required dependencies: "pip install -r requirements.txt"
4. Download redis and activate a local instance using the following command: "redis-server"
5. Verify that you have set the correct values for the following environmental variables:
    - ENVIRONMENT
    - TWITTER_API_KEY
    - TWITTER_API_SECRET
    - TWITTER_CALLBACK
    - TWITCH_API_KEY
    - TWITCH_API_SECRET
    - TWITCH_CALLBACK
    - FRONT_END_URL
    - REDIS_HOST
    - REDIS_PORT
5. Start the server using the command: "flask run"
