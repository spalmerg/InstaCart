# InstaCart Recommender 
Analytics Value Chain Project

## Objective
Create the basic skeleton of a web app that implements a recommender system responding to user input. 

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

    `virtualenv -p python3 Instacart`
    
3. Activate environment

    `source activate Instacart`

4. Install required packages 

    `pip install requirements.txt`

5. Download InstaCart csv files from [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data) and save to Data folder

6. Set up instacart.env file with the following structure to connect to a database instance: 

   ```#!/bin/bash

   export DATABASE_URL= XXX

   export DATABASE=XXX
   export USERNAME=XXX
   export PORT=XXX
   export PASSWORD=XXX
   export HOST=XXX``` 

6. Set your environment
   `source instacart.env`

7. Load database 
    `python create_db.py`
    
8. Create the model 
   ` python model.py`
   
9. Run the app
   `python instaApp.py`

You should be able to go to the IP address that it responds with and see your web app.