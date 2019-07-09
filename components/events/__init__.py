from flask import Flask, render_template, redirect, url_for, flash, Blueprint

import models
from models.ticketbox import db, User, Event, Ticket
from flask_login import current_user

from components.events.form.form import EventForm, TicketForm

events_blueprint=Blueprint('events', __name__, template_folder='templates')


@events_blueprint.route('/delete')
def delte():
    return 'This is DELETE from events blueprint'
    
@events_blueprint.route('/create', methods=['get', 'post'])
def create():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(title=form.title.data,
                        image_url=form.image_url.data,
                        start=form.start.data.strftime('%D'),
                        creator_id=current_user.id,
                        end=form.end.data.strftime('%D'),
                        location=form.location.data,
                        description=form.description.data,
                        price=form.price.data,
                        event_url=form.event_url.data,
                        is_private=form.is_private.data)

        db.session.add(new_event)
        db.session.commit()

        return 'done creatinng new event'

    return render_template('create_event.html', form=form)

@events_blueprint.route('/all')
# @login_required
def event():
    events = Event.query.all()
    # user = User.query.filter_by(id=id).first()
    return render_template('event.html', events = events)

@events_blueprint.route('/<id>')
def viewevent(id):
    event = Event.query.filter_by(id=id).first()
    # user = User.query.filter_by(id=event.creator.id).first()
    user = event.creator
    return render_template('single_event.html', event=event, creator=event.creator.profile)

# @events_blueprint.route('/<id>/purchase', methods=['get', 'post'])
# def purchase(id):
#     if current_user.id is not Event.creator_id:
#         # print(id, current_user.id)
#         new_purchase = Purchase(guest_id=current_user.id, event_id=id)
#         db.session.add(new_purchase)
#         db.session.commit()
#         return 'purchase completed'
#     return render_template('purchase.html')

@events_blueprint.route('/<id>/guest')
def guest(id):
    event = Event.query.filter_by(id=id).first()
    return render_template('guests_list.html', event=event)

@events_blueprint.route('/<id>/edit', methods=['get', 'post'])
def edit(id):
    form = EventForm()
    event = Event.query.filter_by(id=id).first()
    if form.validate_on_submit():
        edited_event = Event(title=form.title.data,
                        image_url=form.image_url.data,
                        creator_id=current_user.id,
                        start=form.start.data.strftime('%Y-%m-%d'),
                        end=form.end.data.strftime('%Y-%m-%d'),
                        location=form.location.data,
                        description=form.description.data,
                        price=form.price.data,
                        event_url=form.event_url.data,
                        is_private=form.is_private.data)

        event.title=edited_event.title
        event.image_url=edited_event.image_url
        event.creator_id=edited_event.creator_id
        event.start=edited_event.start
        event.end=edited_event.end
        event.location=edited_event.location
        event.description=edited_event.description
        event.price=edited_event.price
        event.event_url=edited_event.event_url
        event.is_private=edited_event.is_private

        db.session.commit()

        return 'done udpating new event'

    return render_template('create_event.html', form=form)

@events_blueprint.route('/<id>/delete')
def delete(id):
    event = Event.query.filter_by(id=id).one()

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('events.event'))

@events_blueprint.route('/<id>/add-ticket', methods=['get', 'post'])
def add_ticket(id):
    form = TicketForm()
    if validate_on_submit:

        new_ticket = Ticket(event_id=id,
                            name=form.name.data,
                            price=form.price.data,
                            quantity=form.quantity.data)

        db.session.add(new_ticket)
        db.session.commit()

        return 'tickets created'

    return render_template('create_event.html')

@events_blueprint.route('/<id>/update-ticket', methods=['get', 'post'])
def update_ticket(id):
    form = TicketForm()
    ticket = Ticket.query.filter_by(event_id=id).first()
    if validate_on_submit:

        new_ticket = Ticket(event_id=id,
                            name=form.name.data,
                            price=form.price.data,
                            quantity=form.quantity.data)

        db.session.add(new_ticket)
        db.session.commit()

        return 'tickets created'

    return render_template('create_event.html')


