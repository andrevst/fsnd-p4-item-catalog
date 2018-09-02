#!/usr/bin/env python2

import os

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


# DB Classes to keep data of awesome starships
# user info
# starship category info
class Category(Base):
    __tablename__ = 'ship_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


# starship info
class Starships(Base):

    __tablename__ = 'starship'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category = Column(String(100), ForeignKey('ship_category.name'))
    ship_category = relationship(Category)

# serialize function to be able to send JSON objects
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.ship_category,
        }


engine = create_engine('sqlite:///fleet.db')


Base.metadata.create_all(engine)
