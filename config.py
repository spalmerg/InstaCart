import os

# key for wtforms and enables sessions/cookies for website
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
