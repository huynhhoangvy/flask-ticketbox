# set POSTGRES_USER=postgres
# set POSTGRES_PWD=301194
# set POSTGRES_DB=mydb
# set POSTGRES_HOST=localhost
# set POSTGRES_PORT=5432

# psycopg2
# flask-SQLAlchemy
# flask-migrate


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from flask_apscheduler import APScheduler


from components.users import users_blueprint
from components.events import events_blueprint
from models.ticketbox import User, db, RatingUser


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

bootstrap = Bootstrap(app)

#create connection btw app and login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

#login manager get info abt user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

POSTGRES = {
    'user': 'postgres',
    'pw': '301194',
    'db': 'ticketbox',
    'host': 'localhost',
    'port': '5432'
}

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
# %(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

## FLASK APSCHEDULER ##

# create apcheduler object
scheduler = APScheduler()

# confif our app to woek with the scheduler
# scheduler.init_app(app)

# start scheduler
scheduler.start()

## FLASK APSCHEDULER END ## 


## DEFINE TASK ## 
# @scheduler.task("interval", id='job_1', seconds=10)
# def simple_function():
#     print('hello')

# def send_simple_message():
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandboxa2e1e78d4c5f4dad86622f9dcceb5fd2.mailgun.org/messages",
# 		auth=("api", "48b2f7ff0a74f5b248400ba16ef88c6b-afab6073-738d69bb"),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomness!"})
#####

## forgot password







@app.route('/')
def index():
    return render_template('base.html')


app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(events_blueprint, url_prefix='/events')


if __name__=='__main__':
    app.run(debug=True)