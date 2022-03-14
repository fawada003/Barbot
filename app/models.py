
from datetime import datetime
from app import db

#this file builds our database but does not create it, technically this file isnt needed after creation of db
#obviously its good to have it around to make minor changes and recreate the db afterwards

class Link(db.Model):

    drink_id = db.Column(db.ForeignKey('drink.id'), primary_key=True)
    ingredient_id = db.Column(db.ForeignKey('ingredient.id'), primary_key=True)
    ing_count = db.Column(db.Integer)
    ingredient = db.relationship("Ingredient", back_populates="drinks")
    drink = db.relationship("Drink", back_populates="ingredients")


class Ingredient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    positions = db.relationship("Position", backref="ingredient")
    drinks = db.relationship("Link", back_populates="ingredient")

    def __repr__(self):
        return self.name


class Position(db.Model):

    pos = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey('ingredient.id'), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.pos


class Drink(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    ingredients = db.relationship("Link", back_populates="drink")

    def __repr__(self):
        return '<User %r>' % self.name
