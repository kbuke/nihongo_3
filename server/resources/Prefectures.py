from flask import make_response, session, request
from flask_restful import Resource

from config import db 

from models.Prefecture import PrefectureModel

class PrefectureList(Resource):
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_prefecture = PrefectureModel(
                    prefecture_name = json.get("prefectureName"),
                    kanji = json.get("kanji"),
                    prefecture_img = json.get("prefectureImg"),
                    prefecture_intro = json.get("prefectureIntro")
                )
                db.session.add(new_prefecture)
                db.session.commit()
                return {"message": f"Prefecture created."}
            except ValueError as e:
                return {"error": [str(e)]}
        
