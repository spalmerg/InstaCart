from App import app
import os

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# for elastic beanstalk
application=app

if __name__ == "__main__":
  app.run(debug = True)
