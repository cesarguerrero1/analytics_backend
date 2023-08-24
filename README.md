# Analytics Website Backend

The purpose of this backend is to showcase using Flask to interact with 3rd Party APIs to extract analytical information. That analytical
information will then be consumed via our frontend.

Architecture Patterns: MVCS (Model-View-Service-Controller)
Design Patterns: Factory, Decorator

Gameplan:
1. As a base I want to make sure that a single file Flask App will deploy onto Heroku.
![image](https://github.com/cesarguerrero1/analytics_backend/assets/62967999/ee45b84b-dbea-427a-8a1d-4b12d8a1a778)
2. Once that is verified I will build my file structure and ensure that all of my pages are returning "dummy" data via POSTMAN API calls
3. I will then start connecting my application to Twitter and there will be two major themes:
    a. The first will be making sure that I can appropriately authorize my personal account via this website
    b. The second will be making sure that once I am authorized I can pull analytical data from the site and return it. Again this will be verified with POSTMAN.
4. Once the above is all verified I will be connecting my application to the frontend and handling all of the appropriate routing.


## How to Install Locally
1. On this repository go to Code > Download ZIP
2. Unzip the file in your local directory and then change into the unzipped file
3. From within this directory create a virtual environment and download Python Version: 3.11.4 (This can be found in the runtime.txt file)
4. Use the following command to install all dependencies: pip install -r requirements.txt
5. Run the following command to spin up the local instance: flask --app analytics_api run