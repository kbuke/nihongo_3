from flask import make_response, session, request
from flask_restful import Resource

from config import db

from models.BusinessHours import BusinessHoursModel

from datetime import time, datetime

class BusinessHoursList(Resource):
    def post(self):
        json = request.get_json()
        if json:
            try:
                new_hours = BusinessHoursModel(
                    business_id = json.get("businessId"),
                    applies_to = json.get("appliesTo"),
                    opening_time = json.get("openingTime"),
                    closing_time = json.get("closingTime"),
                    closes_next_day = json.get("closesNextDay")
                )
                db.session.add(new_hours)
                db.session.commit()
                return {"message": "New hours created"}
            except ValueError as e:
                return {"error": [str(e)]}

class BusinessHour(Resource):
    def delete(self, id):
        hour = BusinessHoursModel.query.filter(BusinessHoursModel.id==id).first()
        if hour:
            db.session.delete(hour)
            db.session.commit()
            return {"message": f"Work Hour {id} deleted."}
        else:
            return {"error": f"Could not find Hour {id}"}, 404