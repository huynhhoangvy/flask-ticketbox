from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()



class RatingUser(db.Model):
    __tablename__='rating_users'
    rater_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
        
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    event_created = db.relationship('Event', backref='creator')
    profile = db.relationship('Profile', uselist=False, backref='user')
    ticket = db.relationship('Purchase', backref='owner')
    # event_purchased = db.relationship('Event', secondary='purchases', lazy='subquery', backref=db.backref('buyer', lazy=True))
    # event_purchased = db.relationship('Guest', backref='buyer')
    # ticket = db.relationship('Ticket', backref='buyer')


    rater_id = db.relationship('RatingUser', primaryjoin=(id==RatingUser.rater_id))
    target_user_id = db.relationship('RatingUser', primaryjoin=(id==RatingUser.target_user_id))

    def __repr__(self):
        return "<User{}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Event(db.Model):
    __tablename__='events'
    id = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(999), nullable=False)
    image_url = db.Column(db.String)
    created = db.Column(db.DateTime, server_default=db.func.now())
    start = db.Column(db.DateTime, nullable = False)
    end = db.Column(db.DateTime)
    location = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)
    event_url = db.Column(db.String)
    is_private = db.Column(db.Boolean, default = 0)
    ticket = db.relationship('Ticket', backref='event')
    # discount = db.Column(db.Integer, db.ForeignKey('discount.id'))

class Profile(db.Model):
    __tablename__='profiles'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    avatar_url = db.Column(db.String)
    phone = db.Column(db.Integer)
    about = db.Column(db.String(999), nullable = False)
    address = db.Column(db.String)
    birthdate = db.Column(db.DateTime)
    gender = db.Column(db.Boolean, default=0)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String)
    price = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    date_created = db.Column(db.DateTime)
    payment_method = db.Column(db.String)
    quantity = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    total = db.Column(db.Float)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    











# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(90), nullable = False)

# class EventTag(db.Model):
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

# class Discount(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     name = db.Column(db.String)
#     expiration = db.Column(db.DateTime)
#     effect = db.Column(db.String)

# class EventRating(db.Model):    
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     rating = db.Column(db.Integer)






