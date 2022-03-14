from re import I
from flask import flash, redirect, render_template, request, url_for

from flask_wtf import FlaskForm, Form
from wtforms import FieldList, FormField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField


from app import app, db
import os
from .models import Drink, Ingredient, Link


def choice_query():  # all ingredients for the ingredient select field
    return db.session.query(Ingredient).all()


class IngredientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class InputForm(Form):
    ingredient_name = QuerySelectField(
        query_factory=choice_query, allow_blank=True)
    quantity = SelectField(
        choices=[(1, '2cl'), (2, '4cl'), (3, '6cl')], label="")


class DrinkForm(FlaskForm):
    drink_name = StringField(validators=[DataRequired()], label="")
    ingredients = FieldList(FormField(InputForm), min_entries=6, max_entries=6)
    submit = SubmitField('Submit')


# --------------------- Create Ingredient Page -----------------------------------


@app.route('/create_ingredient', methods=["POST", "GET"])
def create_ingredient():

    form = IngredientForm()
    all_ingredients = Ingredient.query.all()

    print("ingredient page")
    if form.validate_on_submit():
        ingredient_existing = db.session.query(Ingredient).filter(
            Ingredient.name == form.name.data).first()

        if ingredient_existing:
            flash("Ingredient already exists!", "dark")

        else:
            new_ingredient = Ingredient(name=form.name.data)
            db.session.add(new_ingredient)
            db.session.commit()
            flash("Ingredient added!", "success")
            return redirect(url_for('create_ingredient'))

        form.name.data = ""
    return render_template('control/create_ingredient.html', all_ingredients=all_ingredients, form=form)


# ----------------------- Create Drink ------------------------

@app.route('/create_drink',  methods=["POST", "GET"])
def create_drink():
    form = DrinkForm()
    all_links = Link.query.all()
    all_ingredients = Ingredient.query.all()
    all_drinks = Drink.query.all()
    print("drinkpage")

    if request.method == 'POST':

        this_drink = db.session.query(Drink).filter(
            Drink.name == form.drink_name.data).first()

        if this_drink:
            flash("Drink already exists!", "dark")

        else:
            newdrink = Drink(name=form.drink_name.data)

            db.session.add(newdrink)
            print("added")
            for field in form.ingredients:

                # string is needed because of the return value with field.data is int
                string = str(field.ingredient_name.data)
                this_ingredient = db.session.query(Ingredient).filter(
                    Ingredient.name == string).first()
                this_drink = db.session.query(Drink).filter(
                    Drink.name == form.drink_name.data).first()
                if this_ingredient:
                    print("ing")

                    newlink = Link(ingredient_id=this_ingredient.id,
                                   drink_id=this_drink.id, ing_count=field.quantity.data)
                    db.session.add(newlink)
                else:
                    print("pass")

            db.session.commit()
            flash("Drink added!", "success")
            return redirect(url_for('create_drink'))

    return render_template('control/create_drink.html', form=form, all_links=all_links, all_ingredients=all_ingredients, all_drinks=all_drinks)

#---------------- Control Profile ------------------------

@app.route('/control_profile',  methods=["POST", "GET"])
def control_profile():


    return render_template('control/control_profile.html')







@app.route('/shutdown',  methods=["POST", "GET"])
def shutdown():



    return render_template('control/shutdown.html')

@app.route('/confirm_shutdown',  methods=["POST", "GET"])
def confirm_shutdown():


    os.system("sudo shutdown -h now")
    return render_template('control/shutdown.html') 

