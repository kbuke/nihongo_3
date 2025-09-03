from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from models.User import BusinessModel
from models.Industry import IndustryModel

class BusinessIndustryModel(db.Model, SerializerMixin):
    __tablename__ = "business_industries"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    industry_id = db.Column(db. Integer, db.ForeignKey("industries.id"))

    # validate that the business exists
    @validates("business_id")
    def validate_business(self, key, value):
        business = BusinessModel.query.filter(BusinessModel.id==value).first()
        if business:
            return value
        else:
            raise ValueError(f"Business {value} does not exist")
    
    # validate that industry exists
    @validates("industry_id")
    def validate_industry(self, key, value):
        industry = IndustryModel.query.filter(IndustryModel.id==value).first()
        if industry:
            return industry
        else:
            raise ValueError(f"Industry {value} does not exist")