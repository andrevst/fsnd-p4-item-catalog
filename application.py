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

#login configurations here

# main page route

@app.route('/')
@app.route('/starships/')
def showBooks():
    starships = session.query(Starships).all()
    return render_template('starships.html', starships=starships)
    
if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
