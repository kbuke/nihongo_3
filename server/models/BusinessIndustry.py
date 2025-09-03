from config import db
from sqlalchemy_serializer import SerializerMixin

class BusinessIndustryModel(db.Model, SerializerMixin):
    __tablename__ = "business_industries"

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    industry_id = db.Column(db. Integer, db.ForeignKey("industries.id"))
    