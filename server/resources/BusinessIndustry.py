from flask import make_response, session, request
from flask_restful import Resource
from config import db

from models.BusinessIndustry import BusinessIndustryModel

class BusinessIndustryList(Resource):
    def get(self):
        businesses_industries = [industry.to_dict() for industry in BusinessIndustryModel.query.all()]
        return businesses_industries

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

class BusinessIndustry(Resource):
    def patch(self, id):
        data = request.get_json()

        business_industry = BusinessIndustryModel.query.filter(BusinessIndustryModel.id==id).first()
        if business_industry:
            try:
                for attr in data:
                    setattr(business_industry, attr, data[attr])
                db.session.add(business_industry)
                db.session.commit()
                return {"message": f"Update business_industry {id}"}
            except ValueError as e:
                raise {"error": [str(e)]}
        else:
            return {"error": f"business_industry: {id} not found."}, 404
        