from flask import make_response, session, request
from flask_restful import Resource

from config import db

from models.Interests import TravelInterestModel

class TravelInterestList(Resource):
    def get(self):
        interests = [interest.to_dict() for interest in TravelInterestModel.query.all()]
        return interests
    
    def post(self):
        json = request.get_json()
        if json:
            try:
                new_interest = TravelInterestModel(
                    interest = json.get("interest"),
                    img = json.get("interestImg")
                )
                db.session.add(new_interest)
                db.session.commit()
                return {"message": "New interest created"}
            except ValueError as e:
                raise{"error": [str(e)]}