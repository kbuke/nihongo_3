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
    # __mapper_args__ = {
    #     "polymorphic_identity": "user",
    #     "polymorphic_on": ac_type
    # }
