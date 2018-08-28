#!/usr/bin/env python2
# import Flask classes
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from flask import session as login_session
from flask import make_response

# import SqlAlchemy classes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import Database
from db_config import Base, Starships

import random
import string
import httplib2
import json
import requests

# Import security here

app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///fleet.db?check_same_thread=False')
#added ?check_same_thread=False to avoid thread error
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Routes
# main page

@app.route('/')
@app.route('/starships/')
def starshipsCatalog():
    starships = session.query(Starships).all()
    return render_template('starships.html', starships=starships)
    
#Create a newShip

@app.route('/starships/new/', methods=['GET', 'POST'])
def newShip():
    if request.method == 'POST':
        newShip = Starships(name=request.form['name'], description=request.form['description'], category=request.form['category'])
        session.add(newShip)
        session.commit()
        flash("New starship added!")
        return redirect(url_for('starshipsCatalog'))
    else:
        return render_template('newship.html')

# Edit a ship

@app.route('/starships/<int:ship_id>/edit', methods=['GET', 'POST'])
def editShip(ship_id):
    editedShip = session.query(Starships).filter_by(id=ship_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedShip.name = request.form['name']
        if request.form['description']:
            editedShip.description = request.form['description']
        if request.form['category']:
            editedShip.price = request.form['category']
        session.add(editedShip)
        session.commit()
        flash("Starship edited!")
        return redirect(url_for('starshipsCatalog'))
    else:
        return render_template('editship.html', ship_id=ship_id, ship=editedShip)

    
if __name__ == '__main__':
  app.debug = True
  app.secret_key = 'super_secret_key'
  app.run(host = '0.0.0.0', port = 5000)
