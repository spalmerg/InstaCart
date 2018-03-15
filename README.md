# InstaCart Recommender 
Analytics Value Chain Project

## Project Charter
Make recommendations for items a user may want to buy based on the items they are adding to their shopping cart to anticipate items they may want to add, increase app engagement, and ultimately increase order size.

### Vision
Increase app engagement, identify desired items, and ultimately increase order size

### Mission
Increase order size by using recommendations from the user?s current shopping list to suggest missing items or items that the user may want to try, and make adding such items to the shopping list highly accessible to the user

### Success Criteria 
User feedback and assessment logical order product sets

## Package requirements
* [Flask](http://flask.pocoo.org/docs/0.12/)
* [FlaskSQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application)  - 
    * A flask plugin for [SQLAlchemy](http://www.sqlalchemy.org/). SQLAlchemy is an Object Relational Mapper (ORM), which means it allows interaction with relational data models using object oriented approaches, like those typically used in python. 
    * This project uses SQLAlchemy to create, read from, and write to relational databases. 
    * SQLAlchemy's flexibility will allow for a smooth transition from using a local database to using something like Amazon RDS. All that needs to change is a configuration in the app code (see [this blog](https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80) for more on transition to RDS)
* [Surprise](http://surpriselib.com/) 
    * Surprise is a Python scikit building and analyzing recommender systems
    * Surprise is used to build the a collaborative filtering recommender system for the app
 
## Suggested steps

1. Clone repository

2. Create virtual environment for new app 

    ```virtualenv -p python3 Instacart```
    
3. Activate environment

    ```source activate Instacart```

4. Install required packages 

    ```pip install -r requirements.txt```

5. Download InstaCart csv files from [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data) and save to ```analyze/data``` folder

6. Set up instacart.env file with the following structure to connect to a database instance: 

   ```#!/bin/bash

   export DATABASE_URL= XXX

   export DATABASE=XXX
   export USERNAME=XXX
   export PORT=XXX
   export PASSWORD=XXX
   export HOST=XXX`
   
   export SECRET_KEY=XXX`` 

6. Set your environment

   ```source instacart.env```

7. Define database 

    ```python create_db.py```
    
8. Create features, keys, and model by running  ```make all``` from the ```analyze/``` directory

9. Run tests on code

    ```cd analyze/tests```
    ```pytest```
   
10. Run the app by running ```python application.py``` from the root directory

You should be able to go to the IP address that it responds with and see your web app.

To see what it should look like, visit [this link](http://instacart-dev.us-east-2.elasticbeanstalk.com/homepage)

[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2142049)