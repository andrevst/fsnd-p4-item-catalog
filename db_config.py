#!/usr/bin/env python2

import os

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# DB Classes

class Starships(Base):
    
    __tablename__ = 'starships'

    id = Column(Integer, primary_key = True) 
    name = Column(String(80), nullable = False)
    crew = Column(integer(8))
    description = Column(String(250))
    category = Column(String(100), nullable=False)
        
engine = create_engine('sqlite:///starfleet.db')

Base.metadata.create_all(engine)
