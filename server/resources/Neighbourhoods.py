from flask import make_response, session, request
from flask_restful import Resource

from config import db 

from models.Neighbourhoods import NeighbourhoodModel

class NeighbourhoodsList(Resource):
    def get(self):
        neighbourhoods = [neighbourhood.to_dict() for neighbourhood in NeighbourhoodModel.query.all()]
        return neighbourhoods
    
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_neighbourhoods = NeighbourhoodModel(
                    name = json.get("neighbourhoodName"),
                    img = json.get("neighbourhoodImg"),
                    intro = json.get("neighbourhoodIntro"),
                    city_id = json.get("cityId")
                )
                db.session.add(new_neighbourhoods)
                db.session.commit()
                return {"message": "Neighbourhood created"}
            except ValueError as e:
                return {"error": [str(e)]}