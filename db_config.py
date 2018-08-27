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
    
    __tablename__ = 'starship'

    id = Column(Integer, primary_key = True) 
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    category = Column(String(100), nullable=False)
        
#serialize function to be able to send JSON objects 
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            
        }

engine = create_engine('sqlite:///fleet.db')

Base.metadata.create_all(engine)
