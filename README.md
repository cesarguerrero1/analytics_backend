# Analytics Website Backend

The purpose of this backend is to showcase using Flask to interact with 3rd Party APIs such as Twitter and Twitch to extract analytical information about a given user. That analytical information will then be consumed via our frontend to produce a dashboard of data. 

Architecture Patterns: MVCS (Model-View-Service-Controller)
Design Patterns: Factory, Decorator

## Plan:
1. As a base I want to make sure that a single file Flask App will deploy onto Heroku.
2. Once that is verified I will build my file structure and ensure that all of my pages are returning "dummy" data via POSTMAN API calls
3. I will then start connecting my application to Twitter/Twitch and there will be two major themes:
    a. First, I will be making sure that I can appropriately authorize my personal account via thei website
    b. Second, I will be making sure that once I am authorized I can pull analytical data from the site and return it. Again this will be verified with POSTMAN.
4. As I work on those themes I will be using the PyTest and Coverage libraries to unit test our entire application.
    a. In conjunction with the unit tests, I will be using Github Actions to establish a CI/CD pipeline between my application and the Heroku Server where my application is being deployed
5. In the future I will be interacting with the Redis Database to do more than just host the session. I will be adding a persistent element of recording "Contact Us" form submissions.


## How to Install Locally
1. On this repository go to Code > Download ZIP
2. Unzip the file in your local directory and then change into the unzipped file
3. From within this directory create a Virtual Python Environment using the version found in the runtime.txt file
4. Use the following command to install all dependencies: pip install -r requirements.txt
5. Run the following command to spin up the local instance: flask run
6. Be sure to update your environment variables to match the requirements within the code
NOTE: In order to test locally, you will also have to install and startup your own local redis server. The session data in this applicaiton is being handled by Redis.

