from sqlalchemy_serializer import SerializerMixin
from config import db 
from sqlalchemy.orm import validates

class BusinessTypeModel(db.Model, SerializerMixin):
    __tablename__ = "business_types"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)

    # a many-to-many relationship with businesses
        # a business can fall under many types
        # a type can belong to many businesses

    # validate type to ensure no duplicates
    @validates("type")
    def validate_business_type(self, key, value):
        existing_type = BusinessTypeModel.query.filter(BusinessTypeModel.type==value).first()
        if existing_type and existing_type.id != self.id:
            raise ValueError(f"{value} is already registered")
        return value