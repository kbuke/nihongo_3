from models.User import UserModel
from flask import request, make_response, session
from flask_restful import Resource
from config import db

class UserList(Resource):
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_user = UserModel(
                    email = json.get("email"),
                    picture = json.get("profilePicture"),
                    intro = json.get("intro"),
                    ac_type = json.get("acType")
                )
                new_user.password_hash=json.get("newPassword")
                db.session.add(new_user)
                db.session.commit()
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "Failed to add new user"}
