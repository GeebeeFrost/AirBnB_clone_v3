#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from models.place import Place
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def places(self):
            """Returns list of Place instances linked to the City"""
            all_places = models.storage.all(Place).values()
            city_places = [place for place in all_places
                           if place.city_id == self.id]
            return city_places
