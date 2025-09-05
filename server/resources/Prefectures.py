from flask import make_response, session, request
from flask_restful import Resource

from config import db 

from models.Prefecture import PrefectureModel

from sqlalchemy.exc import IntegrityError

class PrefectureList(Resource):
    def get(self):
        prefectures = [prefecture.to_dict() for prefecture in PrefectureModel.query.all()]
        return prefectures

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

class Prefecture(Resource):
    def patch(self, id):
        data = request.get_json()
        prefecture = PrefectureModel.query.filter(PrefectureModel.id==id).first()
        if prefecture:
            try:
                for attr in data:
                    setattr(prefecture, attr, data[attr])
                db.session.add(prefecture)
                db.session.commit()
                return {"message": f"Prefecture {id} info updated."}
            except ValueError as e:
                db.session.rollback()
                return {"error": [str(e)]}, 400
        else:
            return {"error": f"Prefecture {id} not found."}, 404

