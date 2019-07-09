from flask import Flask, render_template, redirect, url_for, flash, Blueprint, current_app

import models
from models.ticketbox import User, db, Event, Profile
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
import requests
from werkzeug.security import generate_password_hash

from components.users.form.form import RegisterForm, LoginForm, ProfileForm, EditForm, EmailForm, PasswordForm

#define blueprint
users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        name=form.name.data,
                        password=form.password.data,
                        email   =form.email.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return 'done signing up'

    return render_template('register.html', form=form)
    
@users_blueprint.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        log_user = User.query.filter_by(username=form.username.data).first()

        if log_user is None:
            redirect(url_for('users.register'))

        if not log_user.check_password(form.password.data):
            return render_template('login.html', form = form)

        login_user(log_user)

        return redirect('/')

    return render_template('login.html', form= form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_blueprint.route('/<id>/created')
def created(id):
    user = User.query.filter_by(id=id).first()
    return render_template('event_created.html', user=user)

@users_blueprint.route('/<id>/purchased')
def purchased(id):
    user = User.query.filter_by(id=id).first()
    return render_template('event_purchased.html', user=user)

@users_blueprint.route('/<id>/update', methods=['get', 'post'])
def update(id):
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        updated_profile = Profile(user_id=id,
                                avatar_url=profile_form.avatar_url.data,
                                phone=profile_form.phone.data,
                                about=profile_form.about.data,
                                address=profile_form.address.data,
                                birthdate=profile_form.birthdate.data.strftime('%Y-%m-%d'),
                                gender=profile_form.gender.data)

        

        db.session.add(updated_profile)
        db.session.commit()

        return 'done generating profile'

    return render_template('update_profile.html', profile_form=profile_form)

@users_blueprint.route('/<id>/edit', methods=['get', 'post'])
def edit(id):
    form = EditForm()

    profile = Profile.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.name=form.name.data
        user.password=form.password.data
        user.email=form.email.data
        
        profile.avatar_url=form.avatar_url.data
        profile.phone=form.phone.data
        profile.about=form.about.data
        profile.address=form.address.data
        profile.birthdate=form.birthdate.data.strftime('%Y-%m-%d')
        profile.gender=form.gender.data

        db.session.commit()

        return 'done editing profile'

    return render_template('register.html', form=form)

@users_blueprint.route('/reset', methods=['post', 'get'])
def reset_password():
    form = EmailForm()
    if form.validate_on_submit():
        #post 
        #validate email
        try:
            User.query.filter_by(email = form.email.data).first_or_404()
        except:
            flash("Invalid email address", 'error')
            return redirect(url_for("users.login"))
        #create token
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = ts.dumps(form.email.data, salt='password_reset_salt')
        password_reset_url = url_for("users.reset_with_token", token=token, _external=True)
        
        password_reset_url = render_template('email_password.html', password_reset_url=password_reset_url)
        print("token: ", token, password_reset_url)


        #send token to this email address
        send_email("reset password", form.email.data, password_reset_url)
        return redirect(url_for('users.login'))
    #get
    return render_template('reset.html', form=form)



MAILGUN_API_KEY='7e91244b71743e7f38608f5c180afbc4-afab6073-dda9a2b0'
MAILGUN_DOMAIN_NAME='sandbox8cb343fab3894ead805ea7bac54d3170.mailgun.org'
def send_email(title, email, html):
        url = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages'
        auth = ('api', MAILGUN_API_KEY)
        data = {
            'from': f'Mailgun User <mailgun@{MAILGUN_DOMAIN_NAME}>',
            'to': email,
            'subject': title,
            'text': 'Plaintext content',
            'html': html
        }
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()

@users_blueprint.route('/reset_token/<token>', methods=['get', 'post'])
def reset_with_token(token):
    try:
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = ts.loads(token, salt='password_reset_salt', max_age=3600)
    except:
        flash("The password reset link is invalid or has expired", 'warning')
        return redirect(url_for('users.login'))

    form = PasswordForm()
    if form.validate_on_submit():
        #post
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('incorrect email!!!', 'warning')
            return redirect(url_for('users.login'))
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    #get
    return render_template('reset_with_token.html',form=form)