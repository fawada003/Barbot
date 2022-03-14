from re import I 

from flask import flash, redirect, render_template, url_for

from flask_wtf import FlaskForm                 #flask wtfform library with useful easy to use forms
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


from .mix import mix                            #function that controls motors
from app import app, db                         

from .models import Drink, Ingredient, Link, Position  #imports db tabels

class IngredientForm(FlaskForm):                                    #creates our form
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

#---------------------- Delete Ingredient --------------------------

@app.route("/delete_ingredient", methods=["GET","POST"])  #app route routes a url on our server
def delete_ingredient():
    
    form = IngredientForm()         
    all_ingredients = Ingredient.query.all()            

    if form.validate_on_submit():

        this_ingredient = Ingredient.query.filter(Ingredient.name == form.name.data).first()
        
        if this_ingredient:   #checks if ingredient with this name exists

            his_positions = db.session.query(Position).filter(Position.ingredient_id == this_ingredient.id).all()
            
            for position in his_positions: #setting all positions to 0 before deleting the Ingredient
                position.ingredient_id = 0

            his_links = db.session.query(Link).filter(Link.ingredient_id == this_ingredient.id).all()

            for link in his_links: #deleting all his links 
                db.session.delete(link)
             
        else:
            flash("The ingredient does not exist", "dark")
            return redirect(url_for('delete_ingredient'))

        db.session.delete(this_ingredient)   

        db.session.commit() 
        flash("Ingredient deleted", "success")
        return redirect(url_for('delete_ingredient'))
    

    return render_template("admin/delete_ingredient.html",form=form, all_ingredients=all_ingredients)



#------------------------- Delete Drinks ---------------------------
@app.route("/delete_drink", methods=["POST","GET"])
def delete_drink():
                                 
    form = IngredientForm()   #altough the name is confusing the already exisiting ingredient form does as good a job as a new one
    all_drinks = Drink.query.all()
    all_links = Link.query.all()
    all_ingredients = Ingredient.query.all()

    if form.validate_on_submit():
        this_drink = db.session.query(Drink).filter(Drink.name == form.name.data).first()
        if this_drink:
            links = db.session.query(Link).filter(Link.drink_id == this_drink.id).all()

            for link in links:
                db.session.delete(link)
                print("link deleted")

            db.session.delete(this_drink)
        
        else:
            flash("Drink does not exist!", "dark")
            return redirect(url_for('delete_drink'))
        
        db.session.commit()
        flash("Drink deleted!", "success")
        return redirect(url_for('delete_drink'))
    return render_template("admin/delete_drink.html", form=form, all_drinks=all_drinks,all_links=all_links,all_ingredients=all_ingredients)


#--------------------  Admin Page ---------------------------

@app.route("/admin_profile", methods=["GET","POST"])
def admin_profile():
 
    return render_template("admin/admin_profile.html")