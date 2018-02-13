import os

# sqlalchemy 
#SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
#SQLALCHEMY_TRACK_MODIFICATIONS = False

# forms
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
