from flask import make_response, session, request
from flask_restful import Resource

from config import db

from models.BusinessHourExceptions import BusinessHourExceptionsModel

from sqlalchemy.exc import IntegrityError

class BusinessHourExceptionList(Resource):
    def get(self):
        business_exceptions = [exception.to_dict() for exception in BusinessHourExceptionsModel.query.all()]
        return business_exceptions
    
    def post(self):
        json = request.get_json()
        
        if json:
            try:
                new_exception = BusinessHourExceptionsModel(
                    date = json.get("date"),
                    is_closed = json.get("closed"),
                    opening_time = json.get("openingTime"),
                    closing_time = json.get("closingTime"),
                    closes_next_day = json.get("closesNextDay"),
                    business_id = json.get("businessId")
                )
                db.session.add(new_exception)
                db.session.commit()
                return {"message": "New business hour exception created."}
            except ValueError as e:
                return{"error": [str(e)]}

class BusinessHourException(Resource):
    def patch(self, id):
        data = request.get_json()

        exception = BusinessHourExceptionsModel.query.filter(BusinessHourExceptionsModel.id==id).first()
        if exception:
            try:
                for attr in data:
                    setattr(exception, attr, data[attr])
                db.session.add(exception)
                db.session.commit()
                return {"message": f"Updated exception {id}"}
            except IntegrityError:
                db.session.rollback()
                return {"error": ["Business already has hours set for this date"]}, 400
        else:
            return {"error": f"Exception {id} not found"}, 404
    
    def delete(self, id):
        exception = BusinessHourExceptionsModel.query.filter(BusinessHourExceptionsModel.id==id).first()
        if exception:
            db.session.delete(exception)
            db.session.commit()
            return {"message": f"Exception {id} deleted."}
        else:
            return {"error": f"Exception {id} not found."}, 404
        