import logging
import threading

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

from flask import flash, redirect, render_template, request, url_for

from flask_wtf import FlaskForm, Form
from sqlalchemy.orm import query  # wtf forms provides easy to use forms
from wtforms import FieldList, FormField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .mix import mix
  
from app import app, db

from .models import Drink, Ingredient, Link, Position
GPIO.setmode(GPIO.BCM)
irsensor = 13# GPIO for button that syncs the x-axis motor
GPIO.setup(irsensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button

working = False   # altough there is propably an inhouse method for checking wether a thread is running this seemed the safest and fastest methdo, let me know waht i missed


def choice_query():                 #needed for query select field 
    return db.session.query(Ingredient).all()


class IngredientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PositionList(Form):
    ingredient_at_position = QuerySelectField(
        query_factory=choice_query, allow_blank=True, label='')


class PositionForm(FlaskForm):
    ingredient = FieldList(FormField(PositionList),
                           min_entries=6, max_entries=6, label="")
    submit = SubmitField('Submit')


class QuantityFreestyle(Form):
    quantity = SelectField(choices=[(0, 'Nothing'), (1, '2cl'), (2, '4cl'), (3, '6cl')], validators=[
                           DataRequired()], label="")


class FreestyleForm(FlaskForm):
    quantities = FieldList(FormField(QuantityFreestyle),
                           min_entries=6, max_entries=6, label="")
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = StringField()
    submit = SubmitField('Submit')


# Thread that runs our mix function in the "background" so the side will reload fast
def thread_function(name, query):
    
   

        logging.info("Thread %s: starting", name)
        mix(query)  # calls the function that moves our motors
        logging.info("Thread %s: finishing", name)

        # with global python know that we dont want to create new var but use the global one
        global working
        # when mix is finished working can be set to False again so we can make an new info
        working = False

   

# ------------------------------- index ------------------------

@app.route('/')
def index():

    print(working)

    return render_template('public/index.html')

# --------------------Order Page ------------------------


@app.route('/order', methods=["POST", "GET"])
def order():
    query = []

    all_drinks = Drink.query.all()
    all_links = Link.query.all()

    all_ingredients = Ingredient.query.all()
    if request.method == 'POST':

        drink_order = Drink.query.filter(
            Drink.name == request.form['submit_button']).first()

        order_links = Link.query.filter(Link.drink_id == drink_order.id).all()

        if order_links:
            for link in order_links:
                this_position = Position.query.filter(
                    Position.ingredient_id == link.ingredient_id).first()

                if this_position:

                    query.append((this_position.pos, link.ing_count))
                    
                else:
                    flash("One of the ingredients has no positon!", "danger")
                    return redirect(url_for('order'))

            global working  # now pyhton know that i want to use the global var instead of creating a new one / not finding one

            if working == False:
                
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(irsensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
                if GPIO.input(irsensor) == GPIO.LOW:
                    working = True
                    format = "%(asctime)s: %(message)s"
                    logging.basicConfig(format=format, level=logging.INFO,
                                        datefmt="%H:%M:%S")
                    logging.info("Main    : before creating thread")
                    x = threading.Thread(target=thread_function, args=(1, query))
                    logging.info("Main    : before running thread")
                    x.start()
                    logging.info("Main    : all done")

                
                    flash("Drink orderd!", "success")
                    return redirect(url_for('order'))
                else:
                    flash("No glass!", "danger")
                    flash("Please place a glass on the robot!", "dark")
                    return redirect(url_for('order'))        

            else:

                flash("Robot is already working!", "danger")
                return redirect(url_for('order'))

        else:

            flash("Drink but contains no ingredients!", "danger")

    return render_template('public/order.html', all_drinks=all_drinks, all_links=all_links, all_ingredients=all_ingredients)

# ----------------- Position Manager ---------------------------------


@app.route('/position_manager', methods=["GET", "POST"])
def position_manager():

    form = PositionForm()
    if form.validate_on_submit():
        for count, field in enumerate(form.ingredient, start=0):

            this_ingredient = db.session.query(Ingredient).filter(
                Ingredient.name == str(field.ingredient_at_position.data)).first()
            if this_ingredient:

                print(this_ingredient.name)

                position_to_update = db.session.query(
                    Position).filter(Position.pos == count).first()

                if position_to_update:
                    position_to_update.ingredient_id = this_ingredient.id
                else:
                    pass

            else:
                pass

        db.session.commit()
        flash("Positions updated!", "success")
        return redirect(url_for('position_manager'))
    return render_template("public/position_manager.html", form=form)


# ----------------------- Freestyle ---------------------

@app.route("/freestyle", methods=["Get", "POST"])
def freestyle():
    form = FreestyleForm()
    query = []
    global working  # so python knows  what var to use

    if form.validate_on_submit():
        for num, field in enumerate(form.quantities, start=1):

            if int(field.quantity.data) == 0:
                print("pass")
            else:
                query.append((num-1, int(field.quantity.data)))

        if working == False:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(irsensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
            if GPIO.input(irsensor) == GPIO.LOW:
                working = True
                format = "%(asctime)s: %(message)s"
                logging.basicConfig(format=format, level=logging.INFO,
                                    datefmt="%H:%M:%S")
                logging.info("Main    : before creating thread")
                x = threading.Thread(target=thread_function, args=(1, query))
                logging.info("Main    : before running thread")
                x.start()
                logging.info("Main    : all done")

                flash("Drink orderd!",  "success")
                return redirect(url_for('order'))
            else:
                flash("No glass!", "danger")
                flash("Please place a glass on the robot!", "dark")
                return redirect(url_for('order'))        

        else:
            flash("Robot is already working!", "danger")
            return redirect(url_for('order'))

    return render_template('public/freestyle.html', form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    users = dict(
        name='passwort',
        name2='passwort',
        name2='passwort',
        name3='passwort',
        name4='passwort',
        name5="teset",
    )

    if form.validate_on_submit():
        if form.username.data == 'Name' and form.password.data == 'Secretkey':
            flash("Welcome home!", "primary")
            return redirect(url_for('admin_profile'))

        else:

            if form.username.data in users:

                if form.password.data == users[form.username.data]:
                    flash("You have logged in!", "primary")
                    return redirect(url_for('control_profile'))

                else:

                    flash("Wrong password!", "danger")
                    return redirect(url_for('login'))

            else:
                flash('No user with this name!', "danger")
                return redirect(url_for('login'))

    return render_template("public/login.html", form=form)
