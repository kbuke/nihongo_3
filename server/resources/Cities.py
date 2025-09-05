from flask import make_response, session, request
from flask_restful import Resource

from config import db

from models.Cities import CitiesModel

class CitiesList(Resource):
    def get(self):
        cities = [city.to_dict() for city in CitiesModel.query.all()]
        return cities
    
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_city = CitiesModel(
                    city_name = json.get("cityName"),
                    city_img = json.get("cityImg"),
                    population = json.get("cityPop"),
                    capital_city = json.get("capitalCity"),
                    prefecture_capital = json.get("prefectureCapital"),
                    city_intro = json.get("cityIntro"),
                    prefecture_id = json.get("prefectureId")
                )
                db.session.add(new_city)
                db.session.commit()
                return {"message": "New city added"}
            except ValueError as e:
                return {"error": [str(e)]}