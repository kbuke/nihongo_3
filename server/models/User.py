from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
import re

class UserModel(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)
    intro = db.Column(db.String, nullable=True)
    ac_type = db.Column(db.String, nullable=False)

    # set up hashing password
    @hybrid_property
    def password_hash(self):
        raise AttributeError
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    # ensure that ac_type is one of three values
    allowed_ac = ["Traveler", "Business", "Admin"]
    @validates("ac_type")
    def validate_ac_type(self, key, value):
        if value not in self.allowed_ac:
            raise ValueError(f"Invalid account type {value}. Must be one of either {self.allowed_ac}")
        return value
    
    # ensure emails are legitimate
    @validates("email")
    def validate_email(self, key, value):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not pattern.match(value):
            raise ValueError("Please enter a valid email address")
        
        # check email is unique
        existing_user = UserModel.query.filter_by(email=value).first()
        if existing_user and existing_user.id != self.id:
            raise ValueError(f"{value} is already registered.")
        return value
    
    # set up polymorphic identities
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": ac_type
    }

class AdminModel(UserModel):
    __tablename__ = "admins"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    name = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "Admin"
    }

class TravelerModel(UserModel):
    __tablename__ = "travelers"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    name = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "Traveler"
    }

class BusinessModel(UserModel):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    business_name = db.Column(db.String, nullable=False)
    open_24hr = db.Column(db.Boolean, nullable=False, default=False)
    allow_email = db.Column(db.Boolean, nullable=False, default=False)

    # address details
    chome = db.Column(db.Integer, nullable=True)
    block = db.Column(db.Integer, nullable=True)
    building_number = db.Column(db.Integer, nullable=True)
    building_name = db.Column(db.String, nullable=True)
    floor = db.Column(db.String, nullable=True)
    room = db.Column(db.String, nullable=True)

    post_code = db.Column(db.String, nullable=False)
    # Japanese postcodes are always 7 chars long
    # Create validation
    @validates("post_code")
    def validate_post_code(self, key, value):
        post_code_pattern = re.compile(r"^\d{3}-?\d{4}$")
        if not post_code_pattern.match(value):
            raise ValueError("Invalid Japanese post code. Must be of type xxx-xxxx or xxxxxxx")
        return value

    # Set up relationship with business types
    industry = db.relationship("IndustryModel", back_populates="business", secondary="business_industries")

    # Set up relationship with business hours
    hours = db.relationship("BusinessHoursModel", back_populates="business")

    serialize_rules = (
        "-industry.business",

        "-hours.business",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "Business"
    }
