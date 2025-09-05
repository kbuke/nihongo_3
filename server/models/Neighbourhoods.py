from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db

class NeighbourhoodModel(db.Model, SerializerMixin):
    __tablename__ = "neighbourhoods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    img = db.Column(db.String)
    intro = db.Column(db.String)

    # set up relations
        # one-to-many
            # a neighbourhood can have many businesses
    businesses = db.relationship("BusinessModel", back_populates="neighbourhood")
            # a neighbourhood belongs to a city
    city_id = db.Column(db.ForeignKey("cities.id"))
    city = db.relationship("CitiesModel", back_populates="neighbourhoods")

    serialize_rules = (
        "-businesses.neighbourhood",
        "-city.neighbourhoods",
    )