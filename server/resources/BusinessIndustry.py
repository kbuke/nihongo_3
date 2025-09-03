from flask import make_response, session, request
from flask_restful import Resource
from config import db

from models.BusinessIndustry import BusinessIndustryModel

class BusinessIndustryList(Resource):
    def post(self):
        json = request.get_json()
        if json:
            try:
                new_business_industry = BusinessIndustryModel(
                    business_id = json.get("businessId"),
                    industry_id = json.get("industryId")
                )
                db.session.add(new_business_industry)
                db.session.commit()
                return {"message": "Created new industry for business."}
            except ValueError as e:
                return {"error": [str(e)]}
        