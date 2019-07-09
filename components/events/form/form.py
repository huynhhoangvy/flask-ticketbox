from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired

class EventForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[InputRequired()])
    start = DateField("Start")
    end = DateField("End")
    location = StringField("Location", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired()])
    # discount_option = StringField("Discount Option", validators=[InputRequired()])
    event_url = StringField("Event URL", validators=[InputRequired()])
    is_private = BooleanField("Privacy")
    submit = SubmitField('Create')

class TicketForm(FlaskForm):
    name = StringField("Name")
    price = FloatField("Price")
    quantity = IntegerField("Quantity")

