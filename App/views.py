from flask import render_template
from App import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('webpage.html',
                           title='Home',
                           user=user)