from models.BusinessType import BusinessTypeModel
from config import db 

from flask_restful import Resource
from flask import make_response, session, request

class BusinessTypeList(Resource):
    def post(self):
        json = request.get_json()
        new_type = json.get("businessType")
        if json:
            try:
                new_type = BusinessTypeModel(
                    type = new_type,
                    img = json.get("businessTypeImg")
                )
                db.session.add(new_type)
                db.session.commit()
                return {"message": f"Business type: {new_type} created."}
            except ValueError as e:
                return {"error": [str(e)]}

class Business(Resource):
    def delete(self, id):
        business = BusinessTypeModel.query.filter(BusinessTypeModel.id==id).first()
        if business:
            db.session.delete(business)
            db.session.commit()
            return {"message": f"Business type {id} deleted."}
        else:
            return {"error": f"Business type {id} not found"}, 404
        