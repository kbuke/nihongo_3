from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db 

from info.prefectures import japanese_prefectures

class PrefectureModel(db.Model, SerializerMixin):
    __tablename__ = "prefectures"

    id = db.Column(db.Integer, primary_key=True)
    prefecture_name = db.Column(db.String, nullable=False, unique=True)
    kanji = db.Column(db.String)
    prefecture_img = db.Column(db.String)
    prefecture_intro = db.Column(db.String)

    # set up relations
        # one-to-many
            # a prefecture can have many businesses
    businesses = db.relationship("BusinessModel", back_populates="prefecture", lazy="dynamic")

            # a prefecture can have many cities
    cities = db.relationship("CitiesModel", back_populates="prefecture", lazy="dynamic")
    

    # Handle serialise rules
        # this one for businesses
    def rmBusinesses(*attributes):
        return tuple(f"-businesses.{attr}" for attr in attributes)

    serialize_rules = (
        *rmBusinesses("hours", "building_number", "industry", "block", "intro", "building_name", "post_code",
            "floor", "allow_email", "_password_hash", "prefecture", "email", "chome", "room"),

        "-cities.prefecture",
    )

    @validates("prefecture_name")
    def validate_name(self, key, value):

        if value not in japanese_prefectures:
            raise ValueError(f"{value} is not a Japanese prefecture.")
        
        existing = PrefectureModel.query.filter(
            PrefectureModel.prefecture_name == value,
            PrefectureModel.id != self.id
        ).first()

        if existing:
            raise ValueError(f"{value} is already registered on the app")
        
        return value
        
    __table_args__ = (
        db.UniqueConstraint("prefecture_name", name="unique_prefecture_name"),
    )


