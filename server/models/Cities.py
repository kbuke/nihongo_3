from config import db 

from sqlalchemy_serializer import SerializerMixin

from sqlalchemy.orm import validates

class CitiesModel(db.Model, SerializerMixin):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)

    city_name = db.Column(db.String)
    city_img = db.Column(db.String)
    population = db.Column(db.String)
    capital_city = db.Column(db.Boolean)
    prefecture_capital = db.Column(db.Boolean)
    city_intro = db.Column(db.String)

    # set up relations
        # one-to-many
            # a prefecture has many cities, a city belongs to a prefecture
    prefecture_id = db.Column(db.ForeignKey("prefectures.id"))
    prefecture = db.relationship("PrefectureModel", back_populates="cities")

            # a city can have many businesses
    businesses = db.relationship("BusinessModel", back_populates="city")

    # set up relationship with neighbourhoods
    neighbourhoods = db.relationship("NeighbourhoodModel", back_populates="city")

    # handle serialization
    

    serialize_rules = (
        "-prefecture.cities",

        "-businesses.city",
        "-businesses.prefecture",

        "-neighbourhoods.city",
    )

    # validate inputs
        # validate population size
    @validates("population")
    def validate_population(self, key, value):
        if isinstance(value, bool):
            raise ValueError("Population must be a numeric value. Not a Boolean")
        
        try:
            pop = int(value) if isinstance(value, str) else value
        except (ValueError, TypeError):
            raise ValueError("Population must be a number")
        
        if not isinstance(pop, int):
            raise ValueError("Population must be an integer")
        
        if not (1000 <= pop <= 999_999_999):
            raise ValueError("A population of a city must be between a thousand and a billion.")
        
        if pop < 1_000_000:
            rounded = round(pop/1000, 2)
            return f"{rounded} Thousand"
        else:
            rounded = round(pop/1_000_000, 2)
            return f"{rounded} Million"