from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email
from models.ticketbox import User

class RegisterForm(FlaskForm):
    username = StringField('User name', validators=[InputRequired()]) 
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Your username has been registered!")
    
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Your email has been registered!")

class LoginForm(FlaskForm):
    username = StringField("User name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):
    avatar_url = StringField('Avatar URL')
    phone = IntegerField('Phone', validators=[InputRequired()]) 
    about = StringField('About')
    address = StringField('Address', validators=[InputRequired()])
    birthdate = DateField('Date of Birth', validators=[InputRequired()])
    gender = BooleanField('Gender: Male', validators=[InputRequired()])
    submit = SubmitField('Update Profile')

class EditForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    avatar_url = StringField('Avatar URL')
    phone = IntegerField('Phone', validators=[InputRequired()]) 
    about = StringField('About')
    address = StringField('Address', validators=[InputRequired()])
    birthdate = DateField('Date of Birth', validators=[InputRequired()])
    gender = BooleanField('Gender: Male', validators=[InputRequired()])
    submit = SubmitField('Update Information')

    # def validate_email(self, field):
    #     if User.query.filter_by(email = field.data).first():
    #         raise ValidationError("Your email has been registered!")

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Forgot Password')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Change Password')

        














