from models.Industry import IndustryModel
from config import db 

from flask_restful import Resource
from flask import make_response, session, request

class IndustryList(Resource):
    def post(self):
        json = request.get_json()
        new_type = json.get("businessType")
        if json:
            try:
                new_type = IndustryModel(
                    type = new_type,
                    img = json.get("businessTypeImg")
                )
                db.session.add(new_type)
                db.session.commit()
                return {"message": f"Business type: {new_type} created."}
            except ValueError as e:
                return {"error": [str(e)]}

class Industry(Resource):
    def delete(self, id):
        business = IndustryModel.query.filter(IndustryModel.id==id).first()
        if business:
            db.session.delete(business)
            db.session.commit()
            return {"message": f"Business type {id} deleted."}
        else:
            return {"error": f"Business type {id} not found"}, 404
        