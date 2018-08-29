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

import random, string

# # importing oauth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

import httplib2
import json
import requests

# app configuration

app = Flask(__name__)

#Google login id's
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Starship Catalog"

# Create session and connect to DB
engine = create_engine('sqlite:///fleet.db?check_same_thread=False')
#added ?check_same_thread=False to avoid thread error
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Login and security
#anti-forgery state token
@app.route('/login')
@app.route('/starships/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done! %s" % data
    return output
    

#Disconnect from Google

@app.route('/gdisconnect')
def gdisconnect():
    #makes sure user are connected
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(json.dumps('User not connected'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'Email is: '
    print login_session['email']
    
    #HTTP GET to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        #reset user session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#Disconnect
@app.route('/disconnect')
@app.route('/starships/disconnect')
def disconnect():
    if 'username' not in login_session:
        print "You were not logged in"
        flash("You were not logged in")
    else:
        gdisconnect()
    return redirect(url_for('starshipsCatalog'))
        
#Routes
#CRUD Functions

#main page (Read all ships)

@app.route('/')
@app.route('/starships/')
def starshipsCatalog():
    if 'email' in login_session:
        print "email is:"
        print login_session['email']
    starships = session.query(Starships).all()
    return render_template('starships.html', starships=starships)
    
#Create a newShip

@app.route('/starships/new/', methods=['GET', 'POST'])
def newShip():
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            newShip = Starships(name=request.form['name'], 
                                description=request.form['description'], 
                                category=request.form['category'])
            session.add(newShip)
            session.commit()
            flash("New starship added!")
            return redirect(url_for('starshipsCatalog'))
        else:
            return render_template('newship.html')

# Edit (Update) a ship

@app.route('/starships/<int:ship_id>/edit', methods=['GET', 'POST'])
def editShip(ship_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
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
            return render_template('editship.html', ship_id=ship_id, 
                                   ship=editedShip)

#Delete Ship

@app.route('/starships/<int:ship_id>/delete/', methods=['GET', 'POST'])
def deleteShip(ship_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        deletedShip = session.query(Starships).filter_by(id=ship_id).one()
        if request.method == 'POST':
            session.delete(deletedShip)
            session.commit()
            flash("Starship deleted!")
            return redirect(url_for('starshipsCatalog'))
        else:
            return render_template('deleteship.html', ship=deletedShip) 

#End of CRUD functions
#JSON API ENDPOINT

#All ships data JSON

@app.route('/starships/JSON')
def starshipsJSON():
    starships = session.query(Starships).all()
    return jsonify(Starships=[i.serialize for i in starships])

#Ship data JSON

@app.route('/starships/<int:ship_id>/JSON')
def starshipJSON(ship_id):
    ship = session.query(Starships).filter_by(id=ship_id).one()
    return jsonify(Starships=ship.serialize)
    
if __name__ == '__main__':
  app.debug = True
  app.secret_key = 'super_secret_key'
  app.run(host = '0.0.0.0', port = 5000)
