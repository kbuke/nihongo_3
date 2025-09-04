from flask import make_response, session, request
from flask_restful import Resource

from config import db

from models.BusinessHourExceptions import BusinessHourExceptionsModel

class BusinessHourExceptionList(Resource):
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
                return {"error": [str(e)]}
        