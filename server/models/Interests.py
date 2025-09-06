from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db

class TravelInterestModel(db.Model, SerializerMixin):
    __tablename__ = "interests"

    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String)
    img = db.Column(db.String)

    # set up relations
        # many-to-many
            # a traveler can have many interests
            # an interest can be shared with many travelers
    
    # set up validations
    @validates("interest")
    def validate_interests(self, key, value):
        if value is None or value == "":
            raise ValueError("Please enter an interest")
        else:
            existing = TravelInterestModel.query.filter(TravelInterestModel.interest==value).first()
            if existing and existing.id != self.id:
                raise ValueError(f"{value} is already registered")
            return value